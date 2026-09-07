#!/usr/bin/env node

import { createHash } from "node:crypto";
import {
  cp,
  mkdir,
  readFile,
  readdir,
  rename,
  rm,
  stat,
  writeFile,
} from "node:fs/promises";
import { homedir } from "node:os";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const packageRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const catalogRoot = join(packageRoot, "skills");
const agentsRoot = join(homedir(), ".agents");
const installRoot = join(agentsRoot, "skills");
const manifestPath = join(installRoot, ".kim-skills.json");
const ignoredNames = new Set([".git", ".DS_Store", "__pycache__"]);

function fail(message) {
  console.error(`Error: ${message}`);
  process.exitCode = 1;
}

async function discoverSkills() {
  const found = new Map();

  async function visit(directory) {
    const entries = await readdir(directory, { withFileTypes: true });
    if (entries.some((entry) => entry.isFile() && entry.name === "SKILL.md")) {
      const skillPath = join(directory, "SKILL.md");
      const content = await readFile(skillPath, "utf8");
      const frontmatter = content.match(/^---\s*\n([\s\S]*?)\n---(?:\s*\n|$)/);
      const nameMatch = frontmatter?.[1].match(/^name:\s*["']?([^"'\n]+?)["']?\s*$/m);
      const name = nameMatch?.[1].trim();

      if (!name || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(name)) {
        throw new Error(`Invalid or missing frontmatter name in ${skillPath}`);
      }
      if (found.has(name)) {
        throw new Error(`Duplicate skill name ${name}`);
      }
      found.set(name, directory);
      return;
    }

    await Promise.all(
      entries
        .filter((entry) => entry.isDirectory() && !ignoredNames.has(entry.name))
        .map((entry) => visit(join(directory, entry.name))),
    );
  }

  await visit(catalogRoot);
  return new Map([...found].sort(([a], [b]) => a.localeCompare(b)));
}

async function readManifest() {
  try {
    const manifest = JSON.parse(await readFile(manifestPath, "utf8"));
    if (
      manifest.version !== 1 ||
      !["all", "selected"].includes(manifest.mode) ||
      !Array.isArray(manifest.skills)
    ) {
      throw new Error("unsupported manifest format");
    }
    return manifest;
  } catch (error) {
    if (error.code === "ENOENT") return null;
    throw new Error(`Cannot read ${manifestPath}: ${error.message}`);
  }
}

async function writeManifest(manifest) {
  await mkdir(installRoot, { recursive: true });
  const temporaryPath = `${manifestPath}.tmp-${process.pid}`;
  await writeFile(temporaryPath, `${JSON.stringify(manifest, null, 2)}\n`);
  await rename(temporaryPath, manifestPath);
}

async function pathExists(path) {
  try {
    await stat(path);
    return true;
  } catch (error) {
    if (error.code === "ENOENT") return false;
    throw error;
  }
}

async function directoryDigest(root) {
  const hash = createHash("sha256");

  async function visit(directory) {
    const entries = (await readdir(directory, { withFileTypes: true })).sort((a, b) =>
      a.name.localeCompare(b.name),
    );
    for (const entry of entries) {
      if (ignoredNames.has(entry.name)) continue;
      const path = join(directory, entry.name);
      const relativePath = relative(root, path);
      if (entry.isDirectory()) {
        hash.update(`d:${relativePath}\n`);
        await visit(path);
      } else if (entry.isFile()) {
        hash.update(`f:${relativePath}\n`);
        hash.update(await readFile(path));
      } else {
        throw new Error(`Unsupported file type: ${path}`);
      }
    }
  }

  await visit(root);
  return hash.digest("hex");
}

async function sameDirectory(left, right) {
  return (await directoryDigest(left)) === (await directoryDigest(right));
}

async function replaceDirectory(source, target) {
  await mkdir(dirname(target), { recursive: true });
  const temporary = `${target}.new-${process.pid}`;
  const backup = `${target}.old-${process.pid}`;
  await rm(temporary, { recursive: true, force: true });
  await rm(backup, { recursive: true, force: true });
  await cp(source, temporary, {
    recursive: true,
    filter: (path) => !ignoredNames.has(path.split("/").at(-1)),
  });

  const existed = await pathExists(target);
  if (existed) await rename(target, backup);
  try {
    await rename(temporary, target);
    await rm(backup, { recursive: true, force: true });
  } catch (error) {
    if (existed && !(await pathExists(target))) await rename(backup, target);
    await rm(temporary, { recursive: true, force: true });
    throw error;
  }
}

async function synchronize(
  catalog,
  manifest,
  requestedMode = manifest?.mode,
  requestedSkills = manifest?.skills ?? [],
) {
  const priorSkills = new Set(manifest?.skills ?? []);
  const desired =
    requestedMode === "all"
      ? new Set(catalog.keys())
      : new Set(requestedSkills.filter((name) => catalog.has(name)));

  const collisions = [];
  for (const name of desired) {
    const target = join(installRoot, name);
    if (
      !priorSkills.has(name) &&
      (await pathExists(target)) &&
      !(await sameDirectory(catalog.get(name), target))
    ) {
      collisions.push(name);
    }
  }
  if (collisions.length) {
    throw new Error(
      `Refusing to overwrite unmanaged skills with different content: ${collisions.join(", ")}`,
    );
  }

  let installed = 0;
  let unchanged = 0;
  for (const name of desired) {
    const source = catalog.get(name);
    const target = join(installRoot, name);
    if ((await pathExists(target)) && (await sameDirectory(source, target))) {
      unchanged += 1;
      continue;
    }
    await replaceDirectory(source, target);
    installed += 1;
  }

  const removed = [];
  for (const name of priorSkills) {
    if (!desired.has(name)) {
      await rm(join(installRoot, name), { recursive: true, force: true });
      removed.push(name);
    }
  }

  const nextManifest = {
    version: 1,
    mode: requestedMode,
    skills: [...desired].sort(),
  };
  await writeManifest(nextManifest);
  console.log(
    `Synchronized ${desired.size} skills (${installed} updated, ${unchanged} unchanged, ${removed.length} removed).`,
  );
}

async function main() {
  const [command = "help", ...args] = process.argv.slice(2);
  const catalog = await discoverSkills();
  const manifest = await readManifest();

  if (command === "list") {
    for (const [name, path] of catalog) {
      const installed = manifest?.skills.includes(name) ? "installed" : "available";
      console.log(`${name}\t${installed}\t${relative(packageRoot, path)}`);
    }
    return;
  }

  if (command === "install") {
    if (args.length === 1 && args[0] === "--all") {
      await synchronize(catalog, manifest, "all");
      return;
    }
    if (!args.length || args.some((name) => !catalog.has(name))) {
      throw new Error("Use install --all or provide valid skill names from the list command");
    }
    const selected = new Set(manifest?.skills ?? []);
    args.forEach((name) => selected.add(name));
    await synchronize(catalog, manifest, "selected", [...selected]);
    return;
  }

  if (command === "sync") {
    if (!manifest) throw new Error("Nothing is managed yet; run install --all or install <name>");
    await synchronize(catalog, manifest, manifest.mode);
    return;
  }

  if (command === "remove") {
    if (!manifest || !args.length) throw new Error("Provide at least one managed skill name");
    const selected = manifest.skills.filter((name) => !args.includes(name));
    await synchronize(catalog, manifest, "selected", selected);
    return;
  }

  console.log(`Usage:
  kim-skills list
  kim-skills install --all
  kim-skills install <skill> [skill...]
  kim-skills sync
  kim-skills remove <skill> [skill...]`);
}

main().catch((error) => fail(error.message));

---
name: to-manual
description: Turn the operations and explanations from this session into a reusable operation manual.
disable-model-invocation: true
---

Write a **reusable** manual from this session: someone facing the same kind of task on a different machine, account, or resource follows it without asking again. The session is the source material; its specific values are a worked example, never the subject.

## 1. Inventory the session

List every operation performed and every explanation given, including detours: failures, their fixes, and why each fix worked. Use any topic list the user supplied as the minimum scope.

Done when each item is tagged **verified** (actually run in this session with observed success) or **unverified** (only described, or run without confirming the result).

## 2. Gate on unverified items

If any item is unverified, list them and ask the user whether to verify them before writing. Wait for the answer. Run, install, or change nothing for verification without that answer; follow the user's choice exactly.

## 3. Generalize

Separate what holds for every instance of the task from what was true only here.

- Replace each session-specific value (names, IDs, IPs, usernames, paths, regions) with a named placeholder such as `<VM_NAME>`, used consistently across every command.
- Open the manual with a placeholder table: placeholder, meaning, how to find its value, and the session's value as the example.
- Add a step for discovering each placeholder's value when the session got it from somewhere the reader must look it up.
- Turn every decision the session made from its own circumstances (this user's account type, this resource's configuration) into a branch: the condition to check and what to do in each case.
- Keep session values only inside placeholder examples and blocks clearly labelled as examples.

Done when every command runs on a different instance by substituting placeholders alone, and every session value sits in an example.

## 4. Write

- **Location:** use the path the user gave; if none, ask. Before writing, read the neighbouring documents and follow their naming, numbering, structure, and language. Point to an existing document for background it already covers.
- **Language:** the user's conversation language.
- **Name** the file and folder for the general task, never for the session's instance.
- **Content**, in order: purpose and prerequisites; placeholder table; steps, each with its verification command and expected result; explanations (the *why* behind non-obvious behaviour); troubleshooting from the failures the session hit; command cheat sheet with placeholders.
- Mark items the user chose to leave unverified as unverified in the manual.

## 5. Report

Give the path and a short outline. Name any remaining unverified items.

# Conceptual Design: `SeedPlanner` Agent (CR-JLS-1005)

This document outlines the conceptual design and operation of the `SeedPlanner` agent, responsible for the autonomous generation of tasks within the Jules ecosystem.

## 1. `src/jules/seed_planner.py` (Conceptual Design)

The `SeedPlanner` agent is envisioned as a Python class, potentially inheriting from a common `AgentBase`.

```python
# Conceptual Python structure for src/jules/seed_planner.py

class SeedPlannerAgent: # (Might inherit from a BaseAgent)
    MAX_OPEN_TASKS = 90
    MAX_TASKS_PER_RUN = 7
    CODEX_FILE_PATH = "CODEX_TASKS.md"
    REFLECTION_LOG_DIR = "archive/"
    SRC_DIR = "src/jules/"
    TESTS_DIR = "tests/jules/"
    AUTO_TASK_PREFIX = "CR-AUTO-"

    def __init__(self):
        # Initialize access to knowledge bases, configuration, etc.
        # Potentially get its own agent definition/tools from AGENTS.md
        self.current_task_id_counter = 0 # Needs a persistent way to track last ID

    def _get_latest_reflection_log(self) -> str:
        # Logic to find the most recent REFLECTION_LOG_*.md in REFLECTION_LOG_DIR
        # Parses and returns relevant content (e.g., open questions, feelings)
        # For simulation, assume it reads the content of the latest log.
        # Example:
        # reflection_files = sorted(glob.glob(f"{self.REFLECTION_LOG_DIR}/REFLECTION_LOG_*.md"))
        # if reflection_files:
        #     with open(reflection_files[-1], 'r') as f:
        #         return f.read()
        return "Conceptual content of latest reflection log." # Placeholder

    def _get_existing_tasks(self) -> tuple[list, int, int]:
        # Logic to read and parse CODEX_TASKS.md
        # Returns a list of existing task IDs, statuses, and potentially titles/details
        # Also determines the highest existing CR-JLS-NNN and CR-AUTO-NNN IDs
        # to ensure new tasks have unique IDs.
        # Example:
        # tasks_details = []
        # open_task_count = 0
        # highest_auto_id = 0
        # with open(self.CODEX_FILE_PATH, 'r') as f:
        #     content = f.read()
        #     # Simplified parsing logic to find task IDs and count open tasks
        #     # In a real scenario, this would involve parsing the full CODEX schema for each task
        #     for match in re.finditer(r"id: (CR-AUTO-(\d+))", content):
        #         if int(match.group(2)) > highest_auto_id:
        #             highest_auto_id = int(match.group(2))
        #     # ... parse other details and count open tasks ...
        # self.current_task_id_counter = highest_auto_id
        # return tasks_details, open_task_count
        # For now, simulate:
        self.current_task_id_counter = 0 # Reset for first conceptual run
        # Simulate that CR-JLS-1001 to CR-JLS-1015 (15 tasks) are present from initial CODEX_TASKS.md population
        # and assume all are "open" for this first run of SeedPlanner.
        return [], 15, 0

    def _analyze_repo_state(self) -> dict:
        # Conceptual analysis of the repository.
        # In a real system, this would use 'git diff', 'ls', file content checks etc.
        # For this conceptual design, we'll simulate findings based on current known state.
        analysis = {
            "core_modules_missing": [],
            "agent_implementations_pending": [],
            "testing_gaps": [],
            "ci_cd_missing": True, # Assume no CI/CD pipeline is defined yet in CODEX_TASKS
        }
        # Heuristic: Check for core orchestrator and config manager
        # Based on current state (src/ is empty except .gitkeep)
        analysis["core_modules_missing"].append("Orchestrator")
        analysis["core_modules_missing"].append("ConfigManager")

        # Heuristic: Check if SeedPlanner itself needs full implementation
        # (This CR-JLS-1005 is just its conceptual design)
        analysis["agent_implementations_pending"].append("SeedPlannerAgent_Internal_Full_Implementation")

        return analysis

    def _generate_task_id(self) -> str:
        self.current_task_id_counter += 1
        return f"{self.AUTO_TASK_PREFIX}{self.current_task_id_counter:03d}"

    def draft_new_tasks(self, reflection_content: str, repo_analysis: dict, existing_tasks: list) -> list:
        new_tasks_content = [] # Will store strings of CODEX tasks

        # Heuristic 1: Core Modules
        if "Orchestrator" in repo_analysis["core_modules_missing"]:
            task_id = self._generate_task_id()
            # This will be one of the example tasks generated below.
            # For now, just conceptual placeholder.
            new_tasks_content.append(f"Placeholder for Orchestrator task with id {task_id}")


        if "ConfigManager" in repo_analysis["core_modules_missing"]:
            task_id = self._generate_task_id()
            # This will be one of the example tasks generated below.
            new_tasks_content.append(f"Placeholder for ConfigManager task with id {task_id}")

        # Heuristic 2: Agent Implementation (SeedPlanner self-implementation)
        if "SeedPlannerAgent_Internal_Full_Implementation" in repo_analysis["agent_implementations_pending"]:
            task_id = self._generate_task_id()
            new_tasks_content.append(f"Placeholder for SeedPlanner full implementation task with id {task_id}")

        # Heuristic 3: CI/CD Setup
        if repo_analysis["ci_cd_missing"]:
            # Check if a CI/CD setup task already exists in CODEX_TASKS.md
            # has_ci_task = any("CI/CD Pipeline" in task.get("title", "") for task in existing_tasks_details) # existing_tasks_details needs to be populated
            # For this simulation, assume it's missing.
            task_id = self._generate_task_id()
            new_tasks_content.append(f"Placeholder for CI/CD setup task with id {task_id}")


        # Heuristic 4: Reflection Driven (from CR-JLS-1004 example)
        if "how will the SeedPlanner agent" in reflection_content.lower() and "effectively translate" in reflection_content.lower():
            task_id = self._generate_task_id()
            # Example: Propose a task to detail its own planning logic if not already robustly defined.
            new_tasks_content.append(f"Placeholder for SeedPlanner Refinement Task based on reflection, id {task_id}")

        # For this conceptual run, we will manually define 1-2 full example tasks later.
        # This function would return a list of fully formatted task strings.
        return [] # Returning empty for now, examples will be manually crafted for the subtask output

    def run_cycle(self):
        # This is a conceptual run for the design document.
        # In a real scenario, this agent would be invoked by a meta-orchestrator.
        print("SeedPlannerAgent: Starting conceptual run cycle...")
        _ , open_task_count, self.current_task_id_counter = self._get_existing_tasks()

        if open_task_count > self.MAX_OPEN_TASKS:
            print(f"SeedPlannerAgent: Open task count ({open_task_count}) exceeds threshold ({self.MAX_OPEN_TASKS}). Skipping new task generation.")
            # In a real system, might log this to SELF_AUDIT.md or notify RoadmapManagerAgent
            return "# Recursion Prevention: Max open tasks exceeded. No new tasks generated.\n"

        reflection_content = self._get_latest_reflection_log()
        repo_analysis = self._analyze_repo_state()

        # For the purpose of this design document, we will show example tasks manually.
        # In a real run, draft_new_tasks would return formatted task strings.
        # newly_drafted_tasks_content = self.draft_new_tasks(reflection_content, repo_analysis, [])
        # if newly_drafted_tasks_content:
        #     # return self._append_tasks_to_codex_content(newly_drafted_tasks_content)
        # else:
        #     return "# No new tasks generated in this cycle by SeedPlanner.\n"
        return "# SeedPlanner conceptual run complete. Example tasks below."


    def _append_tasks_to_codex_content(self, tasks_to_append_strings: list) -> str:
        # This method would generate the actual string to be appended to CODEX_TASKS.md
        # including the header if necessary.
        content_to_append = "\n\n# --- Autogenerated Tasks by SeedPlanner ---\n"
        content_to_append += "# (New tasks will be appended here by SeedPlanner)\n"
        for task_str in tasks_to_append_strings:
            content_to_append += f"\n{task_str}\n---\n"
        return content_to_append

```

## 2. Interaction with `CODEX_TASKS.md`

*   **Reading:** `SeedPlanner` (via its `_get_existing_tasks` method) will read and parse `CODEX_TASKS.md`. This is essential to:
    *   Understand the current workload and avoid proposing duplicate tasks.
    *   Determine the number of open tasks to respect the `MAX_OPEN_TASKS` threshold (recursion prevention).
    *   Find the highest existing `CR-AUTO-XXX` task ID to ensure newly generated tasks receive unique, sequential IDs.
*   **Appending:** Newly generated tasks, formatted as complete CODEX entries, will be appended to the end of the `CODEX_TASKS.md` file.
    *   To distinguish these from manually curated tasks or tasks from other sources, they will be placed under a specific Markdown heading: `# --- Autogenerated Tasks by SeedPlanner ---`.
    *   If this heading is not already present at the end of the file, `SeedPlanner` will add it before appending the first new task. Each task block will be separated by `---`.

## 3. Simulated First Execution Output (Example Tasks)

Given the current repository state (empty `src/` apart from `.gitkeep`, `CODEX_TASKS.md` containing CR-JLS-1001 to CR-JLS-1015, and the first reflection log `archive/REFLECTION_LOG_20250619.md` from CR-JLS-1004), the `SeedPlanner`'s `_analyze_repo_state()` would identify that core modules like an orchestrator and config manager are missing. The reflection log also contains the question: *"How will the SeedPlanner agent (target of CR-JLS-1005) effectively translate the high-level goals of the JULES_LIBERATION_PROMPT into a diverse and actionable initial set of `CODEX_TASKS.md` entries from this corrected blank slate?"*

Here are two plausible tasks `SeedPlanner` would generate and propose for appending to `CODEX_TASKS.md`. (Assuming the initial 15 tasks (CR-JLS-1001 to CR-JLS-1015) are considered "open" for the count, but `SeedPlanner` will generate tasks based on current repo state and reflections).

```markdown
# --- Autogenerated Tasks by SeedPlanner ---
# (New tasks will be appended here by SeedPlanner)

id: CR-AUTO-001
title: Implement Core Application Orchestrator Module
priority: P0
phase: Architecture
category: Enhancement
axis: Reliability
effort: 8
owner_hint: CoreArchAgent_Internal
dependencies: [CR-JLS-1009, CR-AUTO-002] # Depends on AGENTS.md (for CoreArchAgent def) and the Config module
rationale: |
  Current repository analysis via SeedPlanner indicates `src/jules/core/` lacks a central application orchestrator. The JULES_LIBERATION_PROMPT mandates autonomous execution of roadmap tasks, which requires a core component to manage this loop. The first reflection log (archive/REFLECTION_LOG_20250619.md) also highlights anticipation regarding autonomous operations. This task establishes the foundational `Orchestrator` class responsible for loading configurations, initializing agents, fetching tasks from `CODEX_TASKS.md` (via RoadmapManagerAgent_Internal), delegating execution, and managing the overall system lifecycle. This is a critical step for enabling Phase 2 (Execution Loop) of the liberation prompt.
steps: |
  1. Create the directory `src/jules/core/` if it doesn't exist.
  2. Define the `Orchestrator` class in a new file `src/jules/core/orchestrator.py`.
  3. Implement an `__init__` method that loads essential configurations using the `ConfigManager` (from CR-AUTO-002).
  4. Implement a method to initialize core agents (e.g., RoadmapManagerAgent_Internal, EvalAgent_Internal, SelfAuditAgent_Internal) by loading their definitions from `AGENTS.md` and creating instances.
  5. Implement a main `run_execution_loop` method. This loop should:
     a. Query RoadmapManagerAgent_Internal for the next prioritized task from `CODEX_TASKS.md`.
     b. If a task is available, delegate it to the appropriate `owner_hint` agent using the standardized inter-agent communication protocol (CR-JLS-023).
     c. Monitor task status (conceptually, via notifications from the communication bus or by polling).
     d. Handle task completion (success/failure) and log outcomes appropriately using the standardized logging framework (CR-JLS-015).
     e. Implement basic error handling and recovery mechanisms for the loop itself.
  6. Implement methods for graceful startup and shutdown of the Orchestrator and managed agents.
  7. Write comprehensive unit tests for the Orchestrator, covering initialization, task delegation (mocking agent interactions), and state management.
acceptance_criteria: |
  - File `src/jules/core/orchestrator.py` created and committed, containing the `Orchestrator` class structure with methods for initialization, a main execution loop, agent loading, and basic logging.
  - The Orchestrator can be instantiated and its `run_execution_loop` can (in a simulated test) successfully fetch a mock task from a conceptual RoadmapManagerAgent and attempt to delegate it.
  - Unit tests for Orchestrator instantiation, configuration loading, and basic loop control flow achieve >80% coverage.
  - Code includes clear documentation explaining the Orchestrator's role and interaction with other core components.
  - The Orchestrator correctly uses the standardized logging framework for its operational messages.

---
id: CR-AUTO-002
title: Define and Implement Configuration Management Module
priority: P0
phase: Architecture
category: Enhancement
axis: ProcessDebt
effort: 3
owner_hint: CoreArchAgent_Internal
dependencies: [CR-JLS-1009] # Depends on AGENTS.md (for CoreArchAgent def)
rationale: |
  Repository analysis by SeedPlanner shows no dedicated configuration management module in `src/jules/core/`. A centralized and robust system for managing Jules's operational parameters is essential to avoid hardcoding values, which is a source of technical and process debt. This module will handle loading, accessing, and validating configurations such as file paths (e.g., for `CODEX_TASKS.md`, `AGENTS.md`, `SELF_AUDIT.md`), API endpoints (for conceptual external tools or services), feature flags for experimental agent behaviors, and default settings for logging, A/B testing, or resource limits. This improves maintainability, testability, and adaptability of the entire Jules system.
steps: |
  1. Design a schema for Jules's configuration data. Consider using YAML or JSON for file-based configurations. The schema should allow for sections for core system settings, individual agent settings, and potentially environment-specific overrides (e.g., for dev, test, prod self-operation).
  2. Create the file `src/jules/core/config_manager.py`.
  3. Implement a `ConfigManager` class or equivalent functions to:
     a. Load configuration from one or more specified files (e.g., `config/jules_settings.yml`). Support cascading configurations (e.g., base config overridden by environment-specific config).
     b. Provide type-safe methods for easy access to configuration values by other modules and agents (e.g., `config.get_string('logging.level', default='INFO')`, `config.get_int('roadmap.max_open_tasks', required=True)`).
     c. Implement support for default values for non-critical parameters and clear error handling for missing mandatory parameters.
     d. Implement basic validation of configuration values against expected types or ranges.
     e. Log effectively (using CR-JLS-015) when loading configurations, accessing values, or when a requested config value is missing and a default is used.
     f. Consider a mechanism for hot-reloading parts of the configuration if necessary for a long-running system, though this is a P2 requirement.
  4. Create an example default configuration file (e.g., `config/jules_settings.default.yml`) with placeholder values for key parameters identified for the Orchestrator and other bootstrap agents. This file should be committed.
  5. Write comprehensive unit tests for the ConfigManager, verifying correct loading from file, accurate retrieval of values, proper application of defaults, type checking, and robust error handling for missing or malformed configurations.
acceptance_criteria: |
  - File `src/jules/core/config_manager.py` is created and committed, containing a functional configuration management solution.
  - Configuration can be successfully loaded from a sample YAML or JSON file placed in a `config/` directory.
  - Getter methods for configuration values return expected defaults when a value is not in the file, and return the correct loaded value when it is present, with appropriate type casting/conversion.
  - The ConfigManager raises specific, informative errors if a required configuration value is missing or has an invalid type.
  - Unit tests for the ConfigManager achieve >90% code coverage for its core functionalities (loading, getting values, defaults, validation, error handling).
  - An example default configuration file (`config/jules_settings.default.yml`) is created, committed, and includes at least 5 essential configuration parameters for Jules's initial operation.
```

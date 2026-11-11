# Structured Solution Implementation Planning

## Planning Framework

### **Stage One Problem framing**

First, they work out what the problem actually is. This is not yet solution design. It is defining the gap, clarifying who is affected, and identifying constraints, trade-offs, and success conditions. MIT describes problem solving as identifying the problem, developing possible solution paths, and then taking action; MIT also notes that defining the problem includes identifying resources and trade-offs.

### **Stage Two Context building**

Next, they gather the context needed to think well: user needs, environmental conditions, dependencies, evidence, risks, and assumptions. In human-centered design, this corresponds to the early “understand” or “empathize” work before solution generation begins.

### **Stage Three Problem definition**

Then they compress the messy context into a precise statement of the problem to solve. Nielsen Norman Group notes that a problem or user-need statement aligns the team on what is being solved before ideation begins, and that solving the wrong problem will fail even if the solution itself is strong.

### **Stage Four Option generation**

Only after the problem is defined do people start generating candidate solutions. This is divergent thinking: producing multiple approaches rather than locking onto the first plausible answer. NN/g explicitly places ideation before solution prescription and before full prototyping.

### **Stage Five Option evaluation**

After divergence comes convergence. Here, people compare options against constraints, evidence, risks, cost, feasibility, and expected outcomes. This is the stage where assumptions become testable judgments rather than loose intuitions. MIT’s framing of problem solving includes developing possible solution paths and choosing an appropriate course of action.

### **Stage Six Solution structuring**

Once one direction is chosen, the thinking shifts from “Which idea?” to “How would this actually work?” This is where the solution is broken into components, sequence, dependencies, and operating logic. In design-thinking language, this is the transition from ideation into prototype, test, and implementation.

### **Stage Seven Validation**

Before finalizing the plan, humans test whether the proposed structure survives contact with reality. That can mean prototyping, modeling, scenario testing, or checking the plan against edge cases and user feedback. NN/g places testing between prototype and implementation for exactly this reason.

### **Stage Eight Implementation planning**

Only now does the structured implementation plan fully emerge. At this stage the solution becomes an execution artifact: tasks, order of operations, owners, milestones, resources, and decision points. This corresponds to the “implement” or “materialize” phase in established design-process models.

### Summary

The cleanest way to think about the whole process is this:
**understand the problem → define it precisely → generate options → evaluate options → structure the chosen solution → validate it → convert it into an execution plan.** That broad flow is strongly consistent with established problem-solving and design-process models, even though different disciplines use different labels.
The key distinction is that a **structured implementation plan is not the same thing as the solution idea**. It is the downstream artifact produced after framing, analysis, choice, and validation. That is why people often confuse “having an idea” with “being ready to implement,” when those are actually different stages of thinking. This last sentence is an inference from the staged models above.

## Mapping the Framework to the PIV Loop Layer 2 Planning

**PIV layer 2 planning does not sit in just one stage of that framework.** It spans a cluster of stages.

- **Vibe planning** mainly maps to
  **2\. context building**
  **3\. problem definition**
  **4\. option generation**
  **5\. option evaluation**
- **Structured plan generation** mainly maps to
  **6\. solution structuring**
  **7\. validation**
  **8\. implementation planning**
  Put differently:
- vibe planning answers **“what exactly should we build next, and how should we approach it?”**
- structured plan generation answers **“how do we express that chosen approach as a concrete plan that can now be executed safely?”**
  And both are anchored by **1\. problem framing**, because the PRD acts as the North Star for deciding what to build next.

#### Final Mapping

So if I rewrite your original 8-stage framework in PIV layer 2 terms, it becomes:

1. **Problem framing** — inherited from layer 1 / PRD
2. **Context building** — prime, inspect code, read docs, pull context
3. **Problem definition** — define the exact next implementation target
4. **Option generation** — surface multiple approaches
5. **Option evaluation** — compare and choose
6. **Solution structuring** — draft the chosen approach as a plan
7. **Validation** — validate research outputs and the structured plan
8. **Implementation planning** — finalize the execution-ready plan

## Requirements for Effective Vibe Planning

### Stage 2 Context building

**PIV layer 2 term:** early vibe planning

#### Core competencies

The first competency is **context acquisition**: the ability to pull in the right information without drowning in irrelevant detail. That includes reading the PRD, examining the codebase, spotting dependencies, and identifying what is already true versus what is merely assumed.
The second is **signal detection**: noticing what is structurally important. Someone strong here can distinguish core constraints, existing patterns, hidden coupling, and prior decisions from background noise.
The third is **context compression**: turning a large volume of material into a compact internal map of the situation.

#### Necessary mental models

The main mental model here is **orientation before action**. Do not solve yet. Build a map first.
Another key mental model is **systems thinking**. The feature or task sits inside a larger system of constraints, conventions, interfaces, and trade-offs. Good context building means seeing relationships, not just collecting facts.
A third is **evidence over impression**. At this stage, the question is not “what do I think is probably going on?” but “what does the available context actually show?”

#### Mitigate Failure mode

People fail stage 2 when they confuse familiarity with understanding. They skim, recognize a few keywords, and start planning too early.

---

### Stage 3 Problem definition

**PIV layer 2 term:** mid vibe planning, where the next implementation unit is clarified

#### Core competencies

The first competency is **problem slicing**: reducing a broad product need into the next specific implementation-worthy unit.
The second is **constraint articulation**: defining not just what must be built, but what boundaries, assumptions, and non-goals apply.
The third is **outcome clarity**: stating what “done” means for this loop in a way that is specific enough to guide later design choices.

#### Necessary mental models

The key mental model here is **problem precision beats solution enthusiasm**. A badly defined problem can still produce an elegant but useless plan.
Another is **scope discipline**. The right question is not “what all could be done here?” but “what is the exact problem this loop is responsible for solving?”
A third is **boundary thinking**. A good problem definition has edges. It says what is in, what is out, and what belongs to a later loop.

#### Mitigate Failure mode

People fail stage 3 when they define the problem too vaguely, too broadly, or in solution-shaped language. Then later stages become muddy because nobody knows what is actually being chosen between.

---

### Stage 4 Option generation

**PIV layer 2 term:** exploratory vibe planning

#### Core competencies

The first competency is **solution ideation**: producing multiple plausible approaches rather than attaching to the first one.
The second is **design range**: being able to think across different shapes of solution, not just variations of the same idea.
The third is **controlled divergence**: expanding the space of options without losing connection to the defined problem and constraints.

#### Necessary mental models

The central mental model here is **plurality before commitment**. At this stage, the goal is not certainty. It is breadth with relevance.
Another is **possibility thinking under constraint**. Good option generation is not random creativity. It is creativity bounded by the actual problem.
A third is **separation of generation from judgment**. Weak thinkers censor too early. Strong thinkers let candidate options emerge before fully evaluating them.

#### Mitigate Failure mode

People fail stage 4 in two opposite ways: either they generate only one idea, or they generate many ideas with no disciplined connection to the problem definition.

---

### Stage 5 Option evaluation

**PIV layer 2 term:** late vibe planning, where a direction is chosen

#### Core competencies

The first competency is **comparative reasoning**: judging options against each other, not in isolation.
The second is **trade-off analysis**: understanding that most real choices involve gains and losses across simplicity, speed, extensibility, risk, and fit.
The third is **decision-making under uncertainty**: choosing a direction even when not every variable is known.

#### Necessary mental models

The main mental model is **fitness, not perfection**. The question is not “which option is universally best?” but “which option is best for this problem, in this loop, under these constraints?”
Another is **trade-off realism**. Every choice closes off other paths. Good evaluators think in terms of cost, consequences, and downstream effect.
A third is **reversible vs irreversible decision thinking**. If a choice is cheap to change later, you can optimize for speed and simplicity. If it is hard to reverse, you should weigh it more carefully.

#### Mitigate Failure mode

People fail stage 5 when they choose based on taste, novelty, or habit instead of explicit criteria tied to the problem definition and current context.

---

### The deeper pattern across stages 2–5

Taken together, these stages require four higher-order abilities.
First, **epistemic discipline**: knowing the difference between what is known, what is inferred, and what is still unclear.
Second, **scope control**: repeatedly collapsing broadness into the next useful unit.
Third, **structured divergence and convergence**: first widen intelligently, then narrow deliberately.
Fourth, **decision quality under constraint**: selecting a direction that is good enough, justified, and fit for the current loop.

### The simplest way to remember them

- **Stage 2** needs the mind of a **mapper**
- **Stage 3** needs the mind of a **framer**
- **Stage 4** needs the mind of a **designer**
- **Stage 5** needs the mind of a **chooser**
  And in PIV layer 2 terms:
- **context building** = understand the terrain
- **problem definition** = define the exact target
- **option generation** = create plausible paths
- **option evaluation** = choose the path for the structured plan

## Requirements for Effective Structured Planning

### **Stage 6 Solution structuring**

**PIV layer 2 term:** early structured plan generation

#### **Core competencies**

The first competency is **solution architecture**: taking a chosen direction and organizing it into a coherent structure with clear components, responsibilities, and relationships.
The second is **abstraction control**: deciding the right level of detail. Too abstract and the plan is not buildable. Too concrete too early and the plan becomes brittle or prematurely commits to low-level choices.
The third is **integration thinking**: understanding how the chosen solution fits into what already exists, including interfaces, dependencies, data flow, and operational boundaries.
The fourth is **coherence building**: ensuring the parts of the solution actually work together as one design rather than a pile of disconnected implementation ideas.

#### **Necessary mental models**

The key mental model is **from idea to shape**. The goal is no longer to choose a direction. The goal is to give that direction an internal structure.
Another is **systems composition**. A solution is not just a feature list; it is an arrangement of interacting parts.
A third is **structure before sequencing**. Before deciding exactly how to implement, first decide what the solution consists of and how the pieces relate.
A fourth is **fit over elegance**. The best structure is not the most impressive one; it is the one that fits the defined problem, the current architecture, and the implementation constraints.

#### **Failure mode**

People fail stage 6 when they produce something that sounds organized but is not structurally real: vague boxes, hand-wavy components, unclear ownership, missing interfaces, or an overdesigned solution that drifts from the original problem.

---

### **Stage 7 Validation**

**PIV layer 2 term:** late structured plan generation / pre-execution plan testing

#### **Core competencies**

The first competency is **critical challenge**: actively trying to find weaknesses in the solution rather than merely admiring its coherence.
The second is **assumption testing**: identifying what the plan depends on being true and checking whether those assumptions are evidenced, inferred, or still uncertain.
The third is **edge-case reasoning**: stress-testing the solution against failure conditions, unusual inputs, operational constraints, and integration risks.
The fourth is **criteria-based review**: validating the solution against the problem definition, scope boundaries, success criteria, and key constraints rather than against taste.

#### **Necessary mental models**

The central mental model is **try to break it before you build it**. Validation is adversarial in the healthy sense.
Another is **evidence over confidence**. A plan that feels coherent is not necessarily a plan that survives contact with reality.
A third is **failure-first thinking**. Ask where this solution is likely to crack, drift, stall, or overreach.
A fourth is **problem fidelity**. Validation is not only “can this work?” but also “does this still solve the defined problem and only that problem?”

#### **Failure mode**

People fail stage 7 when they treat validation as a rubber stamp. They check for plausibility, not robustness. Or they validate against the wrong thing — for example, against elegance or personal preference instead of the actual problem definition and constraints.

---

### **Stage 8 Implementation planning**

**PIV layer 2 term:** final structured plan generation / execution-ready handoff

#### **Core competencies**

The first competency is **plan decomposition**: breaking the validated solution into executable tasks, phases, and dependencies.
The second is **sequencing judgment**: deciding the right order of operations so work can proceed safely and efficiently.
The third is **delivery shaping**: turning design intent into an implementation path with clear milestones, validation points, and ownership boundaries.
The fourth is **execution realism**: accounting for practical constraints such as testability, rollback, migration risk, dependency ordering, and partial delivery.

#### **Necessary mental models**

The key mental model is **from structure to action**. A good solution shape is not yet an implementation plan.
Another is **dependency-first sequencing**. The order should follow what must exist before something else can be built or verified.
A third is **incremental delivery**. Prefer executable slices and checkpoints over one giant undifferentiated build plan.
A fourth is **plan for learning, not just doing**. Good implementation plans include moments where you validate that the chosen path is still working before sinking more effort into it.

#### **Failure mode**

People fail stage 8 when the plan is either too vague to execute or too rigid to survive reality. Common symptoms are unordered task dumps, missing dependencies, no validation points, hidden prerequisites, and no allowance for partial progress or correction.

### **The deeper pattern across stages 6–8**

Taken together, these stages require four higher-order abilities.
First, **structural rigor**: turning a chosen idea into a real design with parts, boundaries, and relationships.
Second, **adversarial quality control**: pressuring the plan before implementation rather than trusting coherence alone.
Third, **translation from design to execution**: converting a structured solution into buildable work.
Fourth, **reality-sensitive planning**: keeping implementation grounded in dependencies, constraints, and learning loops.

### **The simplest way to remember them**

- **Stage 6** needs the mind of an **architect**
- **Stage 7** needs the mind of a **critic**
- **Stage 8** needs the mind of a **planner**
  And in PIV layer 2 terms:
- **solution structuring** = shape the chosen path
- **validation** = pressure-test the shaped path
- **implementation planning** = turn the validated path into executable work

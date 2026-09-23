# Design and evidence notes

[Case study](README.md) · [Project index](../README.md)

## Source and scope

The reviewed source is the supplied one-page team presentation titled “Ngã tư không ngủ - Vì Dữ liệu luôn thức.” It presents the problem, proposed method, and a SUMO-based illustration.

The source was read as text and inspected visually. No controller code, simulation configuration, traffic inputs, experiment logs, or computer-vision training files were supplied for this project.

The award and personal role are based on previously confirmed profile information. The slide itself is not an award certificate or a record of individual code authorship.

## What the slide supports

| Topic | Present in the slide | What remains unspecified |
| --- | --- | --- |
| Traffic observation | Computer vision converts traffic imagery into numerical information | Detector, tracking method, calibration, and evaluation |
| Traffic-pressure estimate | A density-based quantity is shown for each direction | Operational measurement units, estimator, and update frequency |
| Phase selection | Prioritize the direction/phase with higher pressure; described as Max Pressure | Full controller rule, tie handling, phase-transition logic, and timing constraints |
| Emergency activation | Mentioned as part of the proposed decision logic | Detection method and implemented priority behavior |
| Simulation | SUMO junction illustrations and a comparison narrative | Network and route files, demand scenarios, random seeds, baseline settings, and logs |

This is an inventory of what the presentation communicates, not evidence that each component was implemented and tested.

## Conceptual walkthrough

1. Observe the junction.
2. Convert the observed traffic into a measure for each direction.
3. Compare the directional measures.
4. Use that comparison to inform which phase should receive priority.
5. Assess the resulting behavior in a simulation.

This sequence paraphrases the proposal. It is not an executable control algorithm.

## A possible next prototype

The following is a proposed development plan, separate from the original competition deliverable.

| Work item | Concrete output |
| --- | --- |
| Specify the junction and demand | Versioned simulation network, routes, and scenario descriptions |
| Define a baseline | Explicit fixed-time phases and durations |
| Define the adaptive rule | Documented inputs, phase choices, tie handling, and transition constraints |
| Design the comparison | Matching scenarios and a stated evaluation period for both controllers |
| Record results | Per-run logs, metric definitions, and scripts that regenerate the comparison |
| Test difficult conditions | Scenarios with imbalanced demand, noisy observations, and interrupted inputs |

Any future evaluation should keep the setup and limitations beside the results. A simulation comparison would not by itself establish performance on a real road.

## Contribution boundaries

Nguyễn Thanh Ngân's confirmed contributions are the original idea, problem and solution framing, and participation in presenting or defending the proposal.

The portfolio does not attribute the entire technical implementation to Ngân, infer authorship from the source filename, or claim a deployed traffic-control system.

## Review status

- Reviewed the supplied slide's text and visual content.
- Matched the public summary to the components actually described.
- Kept future prototype work separate from the original deliverable.
- Excluded source files, screenshots, numerical simulation results, and data from the public project folder.

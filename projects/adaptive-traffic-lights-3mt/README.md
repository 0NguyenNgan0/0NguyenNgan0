# Adaptive Traffic Lights
### Faculty-level 3MT 2025 · First Prize · Team project

A research communication project proposing traffic-light timing that responds to changing traffic conditions.

**My role:** originated the idea, framed the problem and proposed solution, and contributed to presenting and defending the proposal.

[Design & evidence](DESIGN_NOTES.md) · [All projects](../README.md) · [Back to my profile](../../README.md)

## The problem

The presentation starts with a familiar situation: a fixed signal schedule can leave traffic waiting even when demand differs between directions. The project asks how observed traffic conditions could inform a more responsive choice of signal phase.

## The proposed approach

The team presentation connects four elements:

| Element | Purpose in the proposal |
| --- | --- |
| Computer vision | Convert observations of traffic into numerical information |
| Direction-level congestion estimate | Summarize traffic pressure for each direction |
| Phase prioritization | Prefer a phase associated with higher pressure, using the slide's Max Pressure framing |
| SUMO simulation | Illustrate fixed timing and flexible coordination in a simulated junction |

The presentation communicates a concept. It does not provide enough implementation detail to reproduce a controller from the slide alone.

## My contribution

- **Original idea:** proposed the adaptive traffic-light concept.
- **Problem framing:** connected rigid signal timing with waiting and unequal traffic demand.
- **Solution framing:** helped organize the idea into observation, measurement, and a control decision.
- **Communication:** contributed to explaining and defending the proposal in a concise presentation.

My contribution centered on the idea and its communication. The computer-vision implementation, controller code, and SUMO experiments are not claimed as work I independently implemented.

## Outcome

The team received **First Prize at the faculty-level 3MT competition in 2025**.

The evidence available for this portfolio is the team presentation and my confirmed role. Simulation figures on the source slide are not republished as verified performance results. No road deployment or measured real-world impact is claimed.

## What this adds to my data portfolio

This project shows the step before model building: choosing a practical problem, identifying what must be observed, and explaining how a data-informed decision might help.

It complements my [forecasting work](../revenue-forecasting-datathon/README.md) and [Tableau case study](../data-explorers-tableau/README.md) through problem framing and technical communication.

## Further development

A reproducible prototype would need documented traffic scenarios, a precise phase-selection rule, signal-transition constraints, and a comparison with a specified baseline. These are next development steps, not completed features.

The [design notes](DESIGN_NOTES.md) distinguish the slide's proposal from that future work.

## Public materials

This page contains a written project description and role attribution. The original slide, simulation screenshots, data, and numerical simulation outputs are not included.

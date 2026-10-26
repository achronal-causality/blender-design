# Design philosophy

Verbatim user statement, preserved from `docs/design-philosophy.md` in the source snapshot. This is a design preference and working premise, not a measured claim of model reliability.

I want to approach graphical design as a programmer and mathematician. My working premise is that ChatGPT is more reliable at coding, mathematical reasoning, and checking explicit relationships than at intuitively choosing spatial coordinates to achieve a particular appearance. The design process should therefore make use of those strengths.

**Creativity should operate primarily at the level of representations, relationships, constraints, and construction rules.** We should define meaningful structures and let the geometry follow from them: symmetry, proportions, connectivity, attachment relationships, surface conditions, and physical mechanisms.

Style is itself a choice. We can deliberately choose ways of representing a subject that work well with mathematical and computational construction. A representation can be expressive and visually successful through the coherence of its rules. This preference should guide our choices where it fits naturally, without forcing every subject into a convenient mathematical form.

The mathematics must also have a defensible connection to what we are representing. Each equation or algorithm should express an identifiable structural relationship, physical mechanism, visual requirement, or deliberate abstraction. Arbitrary functions chosen merely to make the process appear mathematical do not satisfy this principle.

**The goal is to make creative decisions through explicit, intelligible models, derive the detailed geometry from those models, and verify that the result satisfies the intended relationships.**

**My recommendation would be a Blender-native procedural model, authored through Python, with no separate modeling framework initially.** We would add custom mathematical code only when a specific requirement exposes a limitation in the native construction.

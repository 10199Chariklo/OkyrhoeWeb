# ATTRIBUTING 🪐

This project does not build a novel search index, nor does it generate autonomous textual data. **OkyrhoeWeb** operates strictly as an architectural pipeline bridge. Its sole mechanical purpose is to translate public web structures into text primitives for local terminal environments, CLI utilities, and downstream processing software / frameworks.

### 🦆 Foundation Layer: Powered by DuckDuckGo

The entire upstream data layer utilized by this engine is provided by **DuckDuckGo**. 

This engine is built out of deep respect for DuckDuckGo’s clean layout design, lightweight footprints, and historical commitment to user privacy. By prioritizing simple, accessible interfaces like their HTML and **Lite** variants, DuckDuckGo provides an invaluable gateway for lightweight software innovation. 

We explicitly acknowledge that:
1. All search query processing, index lookups, and algorithmic ranking logic are handled entirely by DuckDuckGo.
2. This project acts purely as a local parser, stripping visual formatting layers to make text accessible to low-overhead downstream frameworks.
3. This software is completely unaffiliated with, unauthorized by, and independent of DuckDuckGo.

---

### 🎨 Ethical Representation In Downstream Interfaces

To ensure that the origin of this data is never obscured, misattributed, or passed off as proprietary work, this codebase implements a mandatory formatting invariant. 

Every application, CLI script, or data sheet fueled by this engine must visibly display original source attribution. The engine enforces this by appending a dedicated attribution block straight into the returned result array. Whether displayed in an Excel cell, an agent context payload, or the future text-only **CK Browser**, the structural footprint must explicitly guide users back to the source engine.

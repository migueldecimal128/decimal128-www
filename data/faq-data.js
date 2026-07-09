/*
 * Knowledge base content for the static search feature.
 * This file is loaded as a plain <script> (not fetched as JSON), so the
 * knowledge base page works even when opened directly from disk with no
 * local server, and on GitHub Pages with no build step.
 *
 * To add an entry, copy an existing object in the KB_DATA array below and
 * edit the fields. "category" is used for the filter buttons — reuse an
 * existing category name exactly (including capitalisation) to group entries
 * together, or introduce a new one and it will appear automatically.
 * "links" is optional — an array of { text, url } shown as buttons/links
 * below the answer, e.g. for pointing to external references.
 * "list" is optional — an array of strings shown as a bulleted list below
 * the answer, e.g. for a list of features or guarantees.
 */

const KB_DATA = [
  {
    id: "implementations-1",
    category: "Implementations",
    question: "What are the languages the solution is written in?",
    answer:
      "C, C#, Java, Kotlin KMP, Swift, Rust, Go, and Python.",
    tags: ["languages", "implementations", "cross-platform"]
  },
  {
    id: "benefits-1",
    category: "Benefits",
    question: "How will this decimal128 solution help you?",
    answer: "It will enable a software solution that:",
    list: [
      "Ensures exactness for decimals up to 34 digits of precision",
      "Provides five rounding directions with correct status-flag behavior",
      "Outperforms the IBM (libdecnumber) and Intel (libbid) reference libraries, and Python's libmpdec",
      "Passes all three major industry correctness suites: IBM decTest, IBM fptest, and Intel libbid test vectors",
      "Removes the industry-wide barrier of \"no good decimal option\""
    ],
    tags: ["benefits", "precision", "rounding", "performance", "compliance"]
  },
  {
    id: "resources-1",
    category: "Resources",
    question: "Where can I find out more about decimal128 floating point?",
    answer: "Find more information here:",
    links: [
      {
        text: "Decimal128 floating-point format — Wikipedia",
        url: "https://en.wikipedia.org/wiki/Decimal128_floating-point_format"
      }
    ],
    tags: ["decimal128", "ieee 754", "reference"]
  }
];

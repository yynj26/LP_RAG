CREATE MIGRATION m1nrnc4nxx5svg3kwl3ihbaftsnfbug7b52isjn5di3dxpxma3becq
    ONTO initial
{
  CREATE TYPE default::TextNode {
      CREATE OPTIONAL LINK next: default::TextNode;
      CREATE OPTIONAL LINK previous: default::TextNode;
      CREATE OPTIONAL LINK sources: default::TextNode;
      CREATE REQUIRED PROPERTY endCharIdx: std::int64;
      CREATE OPTIONAL PROPERTY entities: array<std::str>;
      CREATE OPTIONAL PROPERTY excerptKeywords: array<std::str>;
      CREATE REQUIRED PROPERTY filePath: std::str;
      CREATE OPTIONAL PROPERTY prevSectionSummary: std::str;
      CREATE OPTIONAL PROPERTY questionsThisExcerptCanAnswer: array<std::str>;
      CREATE OPTIONAL PROPERTY sectionSummary: std::str;
      CREATE REQUIRED PROPERTY source: std::str;
      CREATE REQUIRED PROPERTY startCharIdx: std::int64;
      CREATE REQUIRED PROPERTY text: std::str;
      CREATE REQUIRED PROPERTY textNodeId: std::str;
      CREATE REQUIRED PROPERTY totalPages: std::int64;
  };
};

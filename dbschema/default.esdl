module default {
    type TextNode {
        required property textNodeId -> str;
        # Metadata fields
        required property source -> str;
        optional property questionsThisExcerptCanAnswer -> array<str>;
        optional property entities -> array<str>;
        optional property prevSectionSummary -> str;
        optional property sectionSummary -> str;
        optional property excerptKeywords -> array<str>;
        # Text content and indices
        required property text -> str;
        optional property startCharIdx -> int64;
        optional property endCharIdx -> int64;
        # Relationships
        optional link sources -> TextNode;
        optional link previous -> TextNode;
        optional link next -> TextNode
    }
}


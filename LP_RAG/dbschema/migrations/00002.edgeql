CREATE MIGRATION m16pw4pjcpyn6zektmpulmwz2yeqpvdg2dttq5be32sbh4gsiaxc2q
    ONTO m1nrnc4nxx5svg3kwl3ihbaftsnfbug7b52isjn5di3dxpxma3becq
{
  ALTER TYPE default::TextNode {
      ALTER PROPERTY endCharIdx {
          SET OPTIONAL;
      };
      DROP PROPERTY filePath;
      ALTER PROPERTY startCharIdx {
          SET OPTIONAL;
      };
      DROP PROPERTY totalPages;
  };
};

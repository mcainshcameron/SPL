-- FantaSPL: Create tables + insert all 40 teams
-- Run in Supabase SQL Editor (https://supabase.com/dashboard → SQL Editor)

CREATE TABLE IF NOT EXISTS fantasy_teams (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  team_name TEXT NOT NULL,
  owner_name TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS fantasy_rosters (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  team_id UUID REFERENCES fantasy_teams(id) ON DELETE CASCADE,
  player_id UUID REFERENCES players(id),
  tier INT NOT NULL,
  price_millions NUMERIC(4,1) NOT NULL
);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Fel Lazio', 'Fabrizio Limonta')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '60b0c592-d285-498d-8e7d-2563e512779d', 1, 2.0),
  ((SELECT id FROM new_team), '80b03638-7dd8-4675-a283-cf602dee92ec', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), '18500146-4204-43c3-90e5-08cc0a033cb7', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '6e9ad2e6-45bb-4650-8e04-f0289c9c3a26', 3, 5.0),
  ((SELECT id FROM new_team), 'b9f8dbc7-c157-4f18-9404-b5b98a9bdff0', 4, 10.0),
  ((SELECT id FROM new_team), 'a5481839-e731-45ee-af3a-9ffb1ce192f1', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Mazzu doveva Vincere', 'Lorenzo Mazzucchelli')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '4af25765-a93a-4643-b150-51c6d15a6d7e', 1, 2.0),
  ((SELECT id FROM new_team), 'a2ea6cec-1937-43ea-a967-70308d477516', 1, 2.0),
  ((SELECT id FROM new_team), '18500146-4204-43c3-90e5-08cc0a033cb7', 2, 7.0),
  ((SELECT id FROM new_team), '6e880191-5138-4430-8266-1b42280da18d', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), '6b8281fe-97a3-46da-bb57-beb42455be47', 4, 10.0),
  ((SELECT id FROM new_team), 'b9f8dbc7-c157-4f18-9404-b5b98a9bdff0', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Latin Supremacy', 'Cristian Diaz Lopez')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '3eba4a4a-484f-4212-9545-a8170a0633d7', 1, 2.0),
  ((SELECT id FROM new_team), '2d818cde-7ad6-49a1-8ef9-c779505c53ad', 1, 2.0),
  ((SELECT id FROM new_team), '6b8281fe-97a3-46da-bb57-beb42455be47', 2, 7.0),
  ((SELECT id FROM new_team), '5e612925-11e0-4890-aee9-0963f00e57a7', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '73289a0f-a512-4d5b-a97f-5728cefcebb7', 3, 5.0),
  ((SELECT id FROM new_team), '7f7ff4ed-6a41-430e-8c16-894545848029', 4, 10.0),
  ((SELECT id FROM new_team), 'ab677fc8-b79c-4fb7-84b9-9064f25ea9a3', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Affori Grizzlies', 'Giovanni Aiello')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '3eba4a4a-484f-4212-9545-a8170a0633d7', 1, 2.0),
  ((SELECT id FROM new_team), '2d818cde-7ad6-49a1-8ef9-c779505c53ad', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), '18500146-4204-43c3-90e5-08cc0a033cb7', 2, 7.0),
  ((SELECT id FROM new_team), '6e9ad2e6-45bb-4650-8e04-f0289c9c3a26', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), '7f7ff4ed-6a41-430e-8c16-894545848029', 4, 10.0),
  ((SELECT id FROM new_team), 'ab677fc8-b79c-4fb7-84b9-9064f25ea9a3', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Limonta United', 'Andrea Limonta')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '80b03638-7dd8-4675-a283-cf602dee92ec', 1, 2.0),
  ((SELECT id FROM new_team), '2d818cde-7ad6-49a1-8ef9-c779505c53ad', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), 'f6034a6b-2bf4-43e2-97b5-355d7e523985', 2, 7.0),
  ((SELECT id FROM new_team), 'f1dfbff8-a17e-435e-8878-921f19f0113d', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), 'b9f8dbc7-c157-4f18-9404-b5b98a9bdff0', 4, 10.0),
  ((SELECT id FROM new_team), '9a28f9a6-e163-4eb4-aac7-a29a86ded9d7', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Omanta', 'Omar Raafat')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '3eba4a4a-484f-4212-9545-a8170a0633d7', 1, 2.0),
  ((SELECT id FROM new_team), '07a3f06c-ce33-4929-b42c-cc890414d136', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), '477fea67-d063-4037-b6bc-ef9c827b381a', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), '7f7ff4ed-6a41-430e-8c16-894545848029', 4, 10.0),
  ((SELECT id FROM new_team), '9a28f9a6-e163-4eb4-aac7-a29a86ded9d7', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Multiple Cancers', 'Federico Lelli')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), 'b0fde0be-8e72-4753-871b-0fa83ac00c1e', 1, 2.0),
  ((SELECT id FROM new_team), 'f09e7857-5fa6-43b9-8325-195c92426069', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), '477fea67-d063-4037-b6bc-ef9c827b381a', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '0ad8edd9-6f9a-42d9-865c-dfe550ba7d40', 3, 5.0),
  ((SELECT id FROM new_team), '7f7ff4ed-6a41-430e-8c16-894545848029', 4, 10.0),
  ((SELECT id FROM new_team), 'ab677fc8-b79c-4fb7-84b9-9064f25ea9a3', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Rapid Viennetta', 'Roberto Janni')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '37335f44-7911-4233-ab37-3059a4a88f92', 1, 2.0),
  ((SELECT id FROM new_team), '07a3f06c-ce33-4929-b42c-cc890414d136', 1, 2.0),
  ((SELECT id FROM new_team), '6e880191-5138-4430-8266-1b42280da18d', 2, 7.0),
  ((SELECT id FROM new_team), '5e612925-11e0-4890-aee9-0963f00e57a7', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), '7f7ff4ed-6a41-430e-8c16-894545848029', 4, 10.0),
  ((SELECT id FROM new_team), 'e4167e31-ddd0-452c-b7ae-2d9270c04f6a', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('T''eamCulo', 'Maurizio Rea')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), 'a1788c76-3335-418c-a3a1-306850b2364a', 1, 2.0),
  ((SELECT id FROM new_team), 'a2ea6cec-1937-43ea-a967-70308d477516', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), 'f6034a6b-2bf4-43e2-97b5-355d7e523985', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), 'b1f902da-3e52-40d1-a05d-86b8ebd7b01f', 4, 10.0),
  ((SELECT id FROM new_team), '9a28f9a6-e163-4eb4-aac7-a29a86ded9d7', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('LA PALLA NON ERA USCITA', 'Ludovico Righi')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), 'f049e7f1-5c3d-4839-a853-744ebe35e08b', 1, 2.0),
  ((SELECT id FROM new_team), '07a3f06c-ce33-4929-b42c-cc890414d136', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), '477fea67-d063-4037-b6bc-ef9c827b381a', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), '9a28f9a6-e163-4eb4-aac7-a29a86ded9d7', 4, 10.0),
  ((SELECT id FROM new_team), 'ab677fc8-b79c-4fb7-84b9-9064f25ea9a3', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Non è la seconda squadra di Mazzu, è la prima', 'Mazzucchello Lorenzi')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '2d818cde-7ad6-49a1-8ef9-c779505c53ad', 1, 2.0),
  ((SELECT id FROM new_team), 'a2ea6cec-1937-43ea-a967-70308d477516', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), '268ee1f3-e095-46bc-8f6a-d8ffc28a2129', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), 'b9f8dbc7-c157-4f18-9404-b5b98a9bdff0', 4, 10.0),
  ((SELECT id FROM new_team), '7f7ff4ed-6a41-430e-8c16-894545848029', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('BARBA FC', 'Damiano Barbanera')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '97dde232-e3d7-4600-8e7a-5190b0cdd95f', 1, 2.0),
  ((SELECT id FROM new_team), 'f09e7857-5fa6-43b9-8325-195c92426069', 1, 2.0),
  ((SELECT id FROM new_team), '477fea67-d063-4037-b6bc-ef9c827b381a', 2, 7.0),
  ((SELECT id FROM new_team), 'f6034a6b-2bf4-43e2-97b5-355d7e523985', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '0ad8edd9-6f9a-42d9-865c-dfe550ba7d40', 3, 5.0),
  ((SELECT id FROM new_team), 'b1f902da-3e52-40d1-a05d-86b8ebd7b01f', 4, 10.0),
  ((SELECT id FROM new_team), 'a5481839-e731-45ee-af3a-9ffb1ce192f1', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('CHIAVO VERONA', 'Sergio Cavalieri')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '3eba4a4a-484f-4212-9545-a8170a0633d7', 1, 2.0),
  ((SELECT id FROM new_team), '2d818cde-7ad6-49a1-8ef9-c779505c53ad', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), '5e612925-11e0-4890-aee9-0963f00e57a7', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), 'b1f902da-3e52-40d1-a05d-86b8ebd7b01f', 4, 10.0),
  ((SELECT id FROM new_team), '9a28f9a6-e163-4eb4-aac7-a29a86ded9d7', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Mazzu è ok', 'Marzio lorenzelli')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '4af25765-a93a-4643-b150-51c6d15a6d7e', 1, 2.0),
  ((SELECT id FROM new_team), '37335f44-7911-4233-ab37-3059a4a88f92', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), '268ee1f3-e095-46bc-8f6a-d8ffc28a2129', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), 'b9f8dbc7-c157-4f18-9404-b5b98a9bdff0', 4, 10.0),
  ((SELECT id FROM new_team), '7f7ff4ed-6a41-430e-8c16-894545848029', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('I nemici di mazzu', 'Arturo Guglielmi')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '30a9c69a-3384-4cea-9d0f-b0fce5efa703', 1, 2.0),
  ((SELECT id FROM new_team), '6b15cdb6-11ef-4c50-ab7b-04652a6a9660', 1, 2.0),
  ((SELECT id FROM new_team), '477fea67-d063-4037-b6bc-ef9c827b381a', 2, 7.0),
  ((SELECT id FROM new_team), 'f6034a6b-2bf4-43e2-97b5-355d7e523985', 2, 7.0),
  ((SELECT id FROM new_team), '33e1d16d-a842-441e-a1bf-5820c60867cc', 3, 5.0),
  ((SELECT id FROM new_team), 'd602c936-cac4-433d-b30d-a72f29d609bd', 3, 5.0),
  ((SELECT id FROM new_team), '7f7ff4ed-6a41-430e-8c16-894545848029', 4, 10.0),
  ((SELECT id FROM new_team), 'ab677fc8-b79c-4fb7-84b9-9064f25ea9a3', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Beverly INPS', 'Federico Paolucci')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '37335f44-7911-4233-ab37-3059a4a88f92', 1, 2.0),
  ((SELECT id FROM new_team), '07a3f06c-ce33-4929-b42c-cc890414d136', 1, 2.0),
  ((SELECT id FROM new_team), '18500146-4204-43c3-90e5-08cc0a033cb7', 2, 7.0),
  ((SELECT id FROM new_team), '6e880191-5138-4430-8266-1b42280da18d', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), 'd30d561e-8d0a-4346-97f8-e3f2017aebae', 4, 10.0),
  ((SELECT id FROM new_team), '97ee86c8-461d-4e2b-a569-499f831f26a6', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Caledonians', 'Ilona Urban')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '2d818cde-7ad6-49a1-8ef9-c779505c53ad', 1, 2.0),
  ((SELECT id FROM new_team), '07a3f06c-ce33-4929-b42c-cc890414d136', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), '477fea67-d063-4037-b6bc-ef9c827b381a', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), 'f1dfbff8-a17e-435e-8878-921f19f0113d', 3, 5.0),
  ((SELECT id FROM new_team), '7f7ff4ed-6a41-430e-8c16-894545848029', 4, 10.0),
  ((SELECT id FROM new_team), 'b1f902da-3e52-40d1-a05d-86b8ebd7b01f', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Fury Bonds', 'Manuel Maimone')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), 'a1788c76-3335-418c-a3a1-306850b2364a', 1, 2.0),
  ((SELECT id FROM new_team), 'bd21375a-b7a3-44dd-a9a8-e96571b06b04', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), '5e612925-11e0-4890-aee9-0963f00e57a7', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), 'd602c936-cac4-433d-b30d-a72f29d609bd', 3, 5.0),
  ((SELECT id FROM new_team), '8bed0ac6-6e52-43bb-b5cc-394ce3735b07', 4, 10.0),
  ((SELECT id FROM new_team), 'bbf3e0c7-5fe5-4207-985a-040f72af33d8', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Cesarino’s', 'Ilaria Pascutti')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '3eba4a4a-484f-4212-9545-a8170a0633d7', 1, 2.0),
  ((SELECT id FROM new_team), 'f09e7857-5fa6-43b9-8325-195c92426069', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), 'f6034a6b-2bf4-43e2-97b5-355d7e523985', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '0ad8edd9-6f9a-42d9-865c-dfe550ba7d40', 3, 5.0),
  ((SELECT id FROM new_team), '8bed0ac6-6e52-43bb-b5cc-394ce3735b07', 4, 10.0),
  ((SELECT id FROM new_team), '8b511d61-7d08-439e-8126-936e1be0a246', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('SPL Solo Per Letette', 'Matteo Ciccaldo')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '08fa69ec-4bd1-4078-a2f8-6fb38a5719a8', 1, 2.0),
  ((SELECT id FROM new_team), '6b15cdb6-11ef-4c50-ab7b-04652a6a9660', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), '6e880191-5138-4430-8266-1b42280da18d', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), '8bed0ac6-6e52-43bb-b5cc-394ce3735b07', 4, 10.0),
  ((SELECT id FROM new_team), '8b511d61-7d08-439e-8126-936e1be0a246', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Football Meta Academy', 'Cormac McAinsh')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), 'a1788c76-3335-418c-a3a1-306850b2364a', 1, 2.0),
  ((SELECT id FROM new_team), '3eba4a4a-484f-4212-9545-a8170a0633d7', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), '6e880191-5138-4430-8266-1b42280da18d', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), 'bbf3e0c7-5fe5-4207-985a-040f72af33d8', 4, 10.0),
  ((SELECT id FROM new_team), '8b511d61-7d08-439e-8126-936e1be0a246', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Artificially Degenerated', 'Cameron McAinsh')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '3e13c327-3caf-4eaf-bac8-bd878c394d6f', 1, 2.0),
  ((SELECT id FROM new_team), '07a3f06c-ce33-4929-b42c-cc890414d136', 1, 2.0),
  ((SELECT id FROM new_team), '268ee1f3-e095-46bc-8f6a-d8ffc28a2129', 2, 7.0),
  ((SELECT id FROM new_team), '18500146-4204-43c3-90e5-08cc0a033cb7', 2, 7.0),
  ((SELECT id FROM new_team), '6e9ad2e6-45bb-4650-8e04-f0289c9c3a26', 3, 5.0),
  ((SELECT id FROM new_team), '73289a0f-a512-4d5b-a97f-5728cefcebb7', 3, 5.0),
  ((SELECT id FROM new_team), 'b9f8dbc7-c157-4f18-9404-b5b98a9bdff0', 4, 10.0),
  ((SELECT id FROM new_team), '9a28f9a6-e163-4eb4-aac7-a29a86ded9d7', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Aldo Ritmo', 'Daniele Miccoli')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '2d818cde-7ad6-49a1-8ef9-c779505c53ad', 1, 2.0),
  ((SELECT id FROM new_team), '07a3f06c-ce33-4929-b42c-cc890414d136', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), 'f6034a6b-2bf4-43e2-97b5-355d7e523985', 2, 7.0),
  ((SELECT id FROM new_team), 'f1dfbff8-a17e-435e-8878-921f19f0113d', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), '9a28f9a6-e163-4eb4-aac7-a29a86ded9d7', 4, 10.0),
  ((SELECT id FROM new_team), 'ab677fc8-b79c-4fb7-84b9-9064f25ea9a3', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Slayer FC', 'Alessio morneghini')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '3e13c327-3caf-4eaf-bac8-bd878c394d6f', 1, 2.0),
  ((SELECT id FROM new_team), 'a2ea6cec-1937-43ea-a967-70308d477516', 1, 2.0),
  ((SELECT id FROM new_team), 'f6034a6b-2bf4-43e2-97b5-355d7e523985', 2, 7.0),
  ((SELECT id FROM new_team), '5e612925-11e0-4890-aee9-0963f00e57a7', 2, 7.0),
  ((SELECT id FROM new_team), '6e9ad2e6-45bb-4650-8e04-f0289c9c3a26', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), 'b9f8dbc7-c157-4f18-9404-b5b98a9bdff0', 4, 10.0),
  ((SELECT id FROM new_team), 'a5481839-e731-45ee-af3a-9ffb1ce192f1', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Foggia', 'Robi Muuu')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '6e474fe2-3936-4d0f-923c-dafaf006bed7', 1, 2.0),
  ((SELECT id FROM new_team), '07a3f06c-ce33-4929-b42c-cc890414d136', 1, 2.0),
  ((SELECT id FROM new_team), '477fea67-d063-4037-b6bc-ef9c827b381a', 2, 7.0),
  ((SELECT id FROM new_team), '18500146-4204-43c3-90e5-08cc0a033cb7', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), 'b9f8dbc7-c157-4f18-9404-b5b98a9bdff0', 4, 10.0),
  ((SELECT id FROM new_team), 'd30d561e-8d0a-4346-97f8-e3f2017aebae', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('NonCiCapiscoNaMazza', 'Guglielmo Bianco')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '60b0c592-d285-498d-8e7d-2563e512779d', 1, 2.0),
  ((SELECT id FROM new_team), '3e13c327-3caf-4eaf-bac8-bd878c394d6f', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), '18500146-4204-43c3-90e5-08cc0a033cb7', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), 'f1dfbff8-a17e-435e-8878-921f19f0113d', 3, 5.0),
  ((SELECT id FROM new_team), 'b1f902da-3e52-40d1-a05d-86b8ebd7b01f', 4, 10.0),
  ((SELECT id FROM new_team), '8b511d61-7d08-439e-8126-936e1be0a246', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('La Paranza Degli Scarponi', 'Willy Rodriguez')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '3eba4a4a-484f-4212-9545-a8170a0633d7', 1, 2.0),
  ((SELECT id FROM new_team), '2d818cde-7ad6-49a1-8ef9-c779505c53ad', 1, 2.0),
  ((SELECT id FROM new_team), '6e880191-5138-4430-8266-1b42280da18d', 2, 7.0),
  ((SELECT id FROM new_team), '5e612925-11e0-4890-aee9-0963f00e57a7', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '33e1d16d-a842-441e-a1bf-5820c60867cc', 3, 5.0),
  ((SELECT id FROM new_team), '7f7ff4ed-6a41-430e-8c16-894545848029', 4, 10.0),
  ((SELECT id FROM new_team), 'ab677fc8-b79c-4fb7-84b9-9064f25ea9a3', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('AC Tua', 'Giulio Pacifico')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '3eba4a4a-484f-4212-9545-a8170a0633d7', 1, 2.0),
  ((SELECT id FROM new_team), '3e13c327-3caf-4eaf-bac8-bd878c394d6f', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), '18500146-4204-43c3-90e5-08cc0a033cb7', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), 'e4167e31-ddd0-452c-b7ae-2d9270c04f6a', 4, 10.0),
  ((SELECT id FROM new_team), 'd1513390-9112-4019-854a-e7ec0e97c85a', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('DAS PORTO', 'Stefano Bolis')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '80b03638-7dd8-4675-a283-cf602dee92ec', 1, 2.0),
  ((SELECT id FROM new_team), 'f09e7857-5fa6-43b9-8325-195c92426069', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), '477fea67-d063-4037-b6bc-ef9c827b381a', 2, 7.0),
  ((SELECT id FROM new_team), '0ad8edd9-6f9a-42d9-865c-dfe550ba7d40', 3, 5.0),
  ((SELECT id FROM new_team), 'd602c936-cac4-433d-b30d-a72f29d609bd', 3, 5.0),
  ((SELECT id FROM new_team), '7f7ff4ed-6a41-430e-8c16-894545848029', 4, 10.0),
  ((SELECT id FROM new_team), '9a28f9a6-e163-4eb4-aac7-a29a86ded9d7', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Rahal Madrid', 'Wissam Rahal')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), 'f049e7f1-5c3d-4839-a853-744ebe35e08b', 1, 2.0),
  ((SELECT id FROM new_team), '31b4ea5e-afcf-4685-8b2b-76aa82157c79', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), '477fea67-d063-4037-b6bc-ef9c827b381a', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), 'bbf3e0c7-5fe5-4207-985a-040f72af33d8', 4, 10.0),
  ((SELECT id FROM new_team), '8b511d61-7d08-439e-8126-936e1be0a246', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Si è girato Mazzoud', 'Franco Abregu Guzman')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), 'b0fde0be-8e72-4753-871b-0fa83ac00c1e', 1, 2.0),
  ((SELECT id FROM new_team), 'f049e7f1-5c3d-4839-a853-744ebe35e08b', 1, 2.0),
  ((SELECT id FROM new_team), 'f6034a6b-2bf4-43e2-97b5-355d7e523985', 2, 7.0),
  ((SELECT id FROM new_team), '6e880191-5138-4430-8266-1b42280da18d', 2, 7.0),
  ((SELECT id FROM new_team), '0ad8edd9-6f9a-42d9-865c-dfe550ba7d40', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), '7f7ff4ed-6a41-430e-8c16-894545848029', 4, 10.0),
  ((SELECT id FROM new_team), 'b1f902da-3e52-40d1-a05d-86b8ebd7b01f', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Calabria Saudita', 'Gianluca Sironi')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '30a9c69a-3384-4cea-9d0f-b0fce5efa703', 1, 2.0),
  ((SELECT id FROM new_team), '07a3f06c-ce33-4929-b42c-cc890414d136', 1, 2.0),
  ((SELECT id FROM new_team), '477fea67-d063-4037-b6bc-ef9c827b381a', 2, 7.0),
  ((SELECT id FROM new_team), '6e880191-5138-4430-8266-1b42280da18d', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), 'd30d561e-8d0a-4346-97f8-e3f2017aebae', 4, 10.0),
  ((SELECT id FROM new_team), 'ab677fc8-b79c-4fb7-84b9-9064f25ea9a3', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('BaffoImpregnato', 'Andrea De Gaetano')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '80b03638-7dd8-4675-a283-cf602dee92ec', 1, 2.0),
  ((SELECT id FROM new_team), 'f5b3711d-350b-4842-9453-5762d5f337bb', 1, 2.0),
  ((SELECT id FROM new_team), '477fea67-d063-4037-b6bc-ef9c827b381a', 2, 7.0),
  ((SELECT id FROM new_team), '6e880191-5138-4430-8266-1b42280da18d', 2, 7.0),
  ((SELECT id FROM new_team), '6e9ad2e6-45bb-4650-8e04-f0289c9c3a26', 3, 5.0),
  ((SELECT id FROM new_team), 'd602c936-cac4-433d-b30d-a72f29d609bd', 3, 5.0),
  ((SELECT id FROM new_team), '9a28f9a6-e163-4eb4-aac7-a29a86ded9d7', 4, 10.0),
  ((SELECT id FROM new_team), 'ab677fc8-b79c-4fb7-84b9-9064f25ea9a3', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Sesso Paperoga Lamborghini', 'Luca Stopelli')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '3eba4a4a-484f-4212-9545-a8170a0633d7', 1, 2.0),
  ((SELECT id FROM new_team), '37335f44-7911-4233-ab37-3059a4a88f92', 1, 2.0),
  ((SELECT id FROM new_team), '18500146-4204-43c3-90e5-08cc0a033cb7', 2, 7.0),
  ((SELECT id FROM new_team), '5e612925-11e0-4890-aee9-0963f00e57a7', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), 'f1dfbff8-a17e-435e-8878-921f19f0113d', 3, 5.0),
  ((SELECT id FROM new_team), 'b9f8dbc7-c157-4f18-9404-b5b98a9bdff0', 4, 10.0),
  ((SELECT id FROM new_team), '97ee86c8-461d-4e2b-a569-499f831f26a6', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('FantasticTeam', 'Camilla Manzo')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), 'a1788c76-3335-418c-a3a1-306850b2364a', 1, 2.0),
  ((SELECT id FROM new_team), 'f5b3711d-350b-4842-9453-5762d5f337bb', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), '6e880191-5138-4430-8266-1b42280da18d', 2, 7.0),
  ((SELECT id FROM new_team), 'f1dfbff8-a17e-435e-8878-921f19f0113d', 3, 5.0),
  ((SELECT id FROM new_team), '73289a0f-a512-4d5b-a97f-5728cefcebb7', 3, 5.0),
  ((SELECT id FROM new_team), '314fedfd-86c4-4eb7-ae9f-d6fef2a4c70d', 4, 10.0),
  ((SELECT id FROM new_team), 'ab677fc8-b79c-4fb7-84b9-9064f25ea9a3', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Damiano Zingaro', 'Federico Petraccia')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '2d818cde-7ad6-49a1-8ef9-c779505c53ad', 1, 2.0),
  ((SELECT id FROM new_team), 'f049e7f1-5c3d-4839-a853-744ebe35e08b', 1, 2.0),
  ((SELECT id FROM new_team), '477fea67-d063-4037-b6bc-ef9c827b381a', 2, 7.0),
  ((SELECT id FROM new_team), 'f6034a6b-2bf4-43e2-97b5-355d7e523985', 2, 7.0),
  ((SELECT id FROM new_team), '0ad8edd9-6f9a-42d9-865c-dfe550ba7d40', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), 'a5481839-e731-45ee-af3a-9ffb1ce192f1', 4, 10.0),
  ((SELECT id FROM new_team), 'e4167e31-ddd0-452c-b7ae-2d9270c04f6a', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('AS TRONZI', 'Mario Croce')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '4af25765-a93a-4643-b150-51c6d15a6d7e', 1, 2.0),
  ((SELECT id FROM new_team), '07a3f06c-ce33-4929-b42c-cc890414d136', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), '6e880191-5138-4430-8266-1b42280da18d', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '6e9ad2e6-45bb-4650-8e04-f0289c9c3a26', 3, 5.0),
  ((SELECT id FROM new_team), '51f9a180-67e3-4733-881e-4094d7de7805', 4, 10.0),
  ((SELECT id FROM new_team), 'a5481839-e731-45ee-af3a-9ffb1ce192f1', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Frozzynone', 'Isabella Daly Forsch')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '2d818cde-7ad6-49a1-8ef9-c779505c53ad', 1, 2.0),
  ((SELECT id FROM new_team), '37335f44-7911-4233-ab37-3059a4a88f92', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), '477fea67-d063-4037-b6bc-ef9c827b381a', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), 'bbf3e0c7-5fe5-4207-985a-040f72af33d8', 4, 10.0),
  ((SELECT id FROM new_team), 'e4167e31-ddd0-452c-b7ae-2d9270c04f6a', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Olesto', 'Martina Perfetto')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), '37335f44-7911-4233-ab37-3059a4a88f92', 1, 2.0),
  ((SELECT id FROM new_team), '07a3f06c-ce33-4929-b42c-cc890414d136', 1, 2.0),
  ((SELECT id FROM new_team), '8fbeb291-63c7-459d-81e9-b83bb2efe107', 2, 7.0),
  ((SELECT id FROM new_team), '5e612925-11e0-4890-aee9-0963f00e57a7', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), 'a5481839-e731-45ee-af3a-9ffb1ce192f1', 4, 10.0),
  ((SELECT id FROM new_team), '9a28f9a6-e163-4eb4-aac7-a29a86ded9d7', 4, 10.0);

WITH new_team AS (
  INSERT INTO fantasy_teams (team_name, owner_name)
  VALUES ('Quant''è bello Damiano in canotta', 'Renzo Micchuzzella')
  RETURNING id
)
INSERT INTO fantasy_rosters (team_id, player_id, tier, price_millions) VALUES
  ((SELECT id FROM new_team), 'f09e7857-5fa6-43b9-8325-195c92426069', 1, 2.0),
  ((SELECT id FROM new_team), '08fa69ec-4bd1-4078-a2f8-6fb38a5719a8', 1, 2.0),
  ((SELECT id FROM new_team), '268ee1f3-e095-46bc-8f6a-d8ffc28a2129', 2, 7.0),
  ((SELECT id FROM new_team), '6e880191-5138-4430-8266-1b42280da18d', 2, 7.0),
  ((SELECT id FROM new_team), '62b786d2-30f2-43cf-b562-e350b45bc8a4', 3, 5.0),
  ((SELECT id FROM new_team), '54a50690-e35a-40d8-bd04-765cdcc48d31', 3, 5.0),
  ((SELECT id FROM new_team), 'b9f8dbc7-c157-4f18-9404-b5b98a9bdff0', 4, 10.0),
  ((SELECT id FROM new_team), 'f8bfd1f5-e380-4977-beba-3124c9415f04', 4, 10.0);


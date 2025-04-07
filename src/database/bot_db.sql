INSERT INTO manager (name, tg_id, role)
VALUES ('mabus777', 878051383, 'admin');


ALTER TABLE manager
ALTER COLUMN tg_id DROP NOT NULL;


ALTER TABLE Users ADD COLUMN registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;



INSERT INTO Users (tg_id, balance, yandex_calendar, code_autorization_google, name, registration_date)
VALUES
(1001, 50.00, 'calendar_link_1', 'code1', 'UserOne', CURRENT_DATE - INTERVAL '1 day'),
(1002, 20.00, 'calendar_link_2', 'code2', 'UserTwo', CURRENT_DATE - INTERVAL '2 day'),
(1003, 0.00, 'calendar_link_3', 'code3', 'UserThree', CURRENT_DATE - INTERVAL '5 day'),
(1004, 100.00, NULL, '', 'UserFour', CURRENT_DATE - INTERVAL '7 day'),
(1005, 75.00, NULL, '', 'UserFive', CURRENT_DATE);


INSERT INTO Paths (citys, user_id)
VALUES
(ARRAY['Moscow', 'Kazan', 'Sochi'], 1001),
(ARRAY['Moscow', 'Saint Petersburg'], 1002),
(ARRAY['Kazan', 'Novosibirsk'], 1003),
(ARRAY['Sochi', 'Moscow'], 1004),
(ARRAY['Kazan', 'Sochi'], 1005);



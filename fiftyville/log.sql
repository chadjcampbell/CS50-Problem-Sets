-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT description
  FROM crime_scene_reports
 WHERE month = 7 AND day = 28 AND street = "Humphrey Street";

Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses
who were present at the time – each of their interview transcripts mentions the bakery.
Littering took place at 16:36. No known witnesses.

SELECT * FROM interviews WHERE month = 7 AND day  = 28 AND transcript LIKE "%bakery%";

ID    Name               Date
 161 | Ruth    | 2021 | 7     | 28  | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
 162 | Eugene  | 2021 | 7     | 28  | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at
Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
 163 | Raymond | 2021 | 7     | 28  | As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
The thief then asked the person on the other end of the phone to purchase the flight ticket. |
 193 | Emma    | 2021 | 7     | 28  | I'm the bakery owner, and someone came in, suspiciously whispering into a phone for about half an hour.
They never bought anything.

SELECT * FROM phone_calls WHERE month = 7 AND day  = 28 AND duration < 60;

+-----+----------------+----------------+------+-------+-----+----------+
| id  |     caller     |    receiver    | year | month | day | duration |
+-----+----------------+----------------+------+-------+-----+----------+
| 221 | (130) 555-0289 | (996) 555-8899 | 2021 | 7     | 28  | 51       |
| 224 | (499) 555-9472 | (892) 555-8872 | 2021 | 7     | 28  | 36       |
| 233 | (367) 555-5533 | (375) 555-8161 | 2021 | 7     | 28  | 45       |
| 251 | (499) 555-9472 | (717) 555-1342 | 2021 | 7     | 28  | 50       |
| 254 | (286) 555-6063 | (676) 555-6554 | 2021 | 7     | 28  | 43       |
| 255 | (770) 555-1861 | (725) 555-3243 | 2021 | 7     | 28  | 49       |
| 261 | (031) 555-6622 | (910) 555-3251 | 2021 | 7     | 28  | 38       |
| 279 | (826) 555-1652 | (066) 555-9701 | 2021 | 7     | 28  | 55       |
| 281 | (338) 555-6650 | (704) 555-2131 | 2021 | 7     | 28  | 54       |
+-----+----------------+----------------+------+-------+-----+----------+

SELECT * FROM atm_transactions WHERE month = 7 AND day  = 28 AND atm_location = "Leggett Street";

+-----+----------------+------+-------+-----+----------------+------------------+--------+
| id  | account_number | year | month | day |  atm_location  | transaction_type | amount |
+-----+----------------+------+-------+-----+----------------+------------------+--------+
| 246 | 28500762       | 2021 | 7     | 28  | Leggett Street | withdraw         | 48     |
| 264 | 28296815       | 2021 | 7     | 28  | Leggett Street | withdraw         | 20     |
| 266 | 76054385       | 2021 | 7     | 28  | Leggett Street | withdraw         | 60     |
| 267 | 49610011       | 2021 | 7     | 28  | Leggett Street | withdraw         | 50     |
| 269 | 16153065       | 2021 | 7     | 28  | Leggett Street | withdraw         | 80     |
| 275 | 86363979       | 2021 | 7     | 28  | Leggett Street | deposit          | 10     |
| 288 | 25506511       | 2021 | 7     | 28  | Leggett Street | withdraw         | 20     |
| 313 | 81061156       | 2021 | 7     | 28  | Leggett Street | withdraw         | 30     |
| 336 | 26013199       | 2021 | 7     | 28  | Leggett Street | withdraw         | 35     |
+-----+----------------+------+-------+-----+----------------+------------------+--------+

SELECT * FROM bank_accounts WHERE account_number IN (
SELECT account_number FROM atm_transactions WHERE month = 7 AND day  = 28 AND atm_location = "Leggett Street");
-- Link accounts to people

SELECT name FROM people WHERE id IN (
SELECT person_id FROM bank_accounts WHERE account_number IN (
SELECT account_number FROM atm_transactions WHERE month = 7 AND day  = 28 AND atm_location = "Leggett Street"))
AND phone_number IN (SELECT caller FROM phone_calls WHERE month = 7 AND day  = 28 AND duration < 60);
--People that were on the caller list & atm list

+---------+
|  name   |
+---------+
| Kenny   |
| Benista |
| Taylor  |
| Diana   |
| Bruce   |
+---------+

SELECT * FROM flights WHERE origin_airport_id = 8 AND day = 29;
-- Earliest flight out was flight id# 36 - Destination LaGuardia Airport, New York City

SELECT name FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36);
-- People on that flight
+--------+
|  name  |
+--------+
| Kenny  |
| Sofia  |
| Taylor |
| Luca   |
| Kelsey |
| Edward |
| Bruce  |
| Doris  |
+--------+

-- ** These people were on that flight, and the outbound caller and ATM log
SELECT * FROM people WHERE name = "Kenny" OR name = "Taylor" OR name = "Bruce";
+--------+--------+----------------+-----------------+---------------+
|   id   |  name  |  phone_number  | passport_number | license_plate |
+--------+--------+----------------+-----------------+---------------+
| 395717 | Kenny  | (826) 555-1652 | 9878712108      | 30G67EN       |
| 449774 | Taylor | (286) 555-6063 | 1988161715      | 1106N58       |
| 686048 | Bruce  | (367) 555-5533 | 5773159633      | 94KL13X       |
+--------+--------+----------------+-----------------+---------------+

SELECT * FROM bakery_security_logs WHERE license_plate IN (
SELECT license_plate FROM people WHERE name = "Kenny" OR name = "Taylor" OR name = "Bruce")
AND day = 28;
+-----+------+-------+-----+------+--------+----------+---------------+
| id  | year | month | day | hour | minute | activity | license_plate |
+-----+------+-------+-----+------+--------+----------+---------------+
| 232 | 2021 | 7     | 28  | 8    | 23     | entrance | 94KL13X       |
| 237 | 2021 | 7     | 28  | 8    | 34     | entrance | 1106N58       |
| 261 | 2021 | 7     | 28  | 10   | 18     | exit     | 94KL13X       |
| 268 | 2021 | 7     | 28  | 10   | 35     | exit     | 1106N58       |
+-----+------+-------+-----+------+--------+----------+---------------+
-- Taylor and Bruce were at the bakery, made a sub 60 second call, were at the ATM on Leggett, and on the flight
-- BUT, Bruce was the one that left within 10 minutes of the theft

-- (375) 555-8161 was the receiver of Bruces call

SELECT name, phone_number FROM people WHERE phone_number = "(375) 555-8161";
-- Robin is the accomplice

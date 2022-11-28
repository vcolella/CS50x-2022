-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Crimes commited on July 28, 2021 on Humphrey Street
    SELECT id, description FROM crime_scene_reports WHERE month = 7 AND day = 28 AND year = 2021 AND street = "Humphrey Street";

    -- outputs :
    -- | 295 | Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery. |

-- Interviews with witnesses
    SELECT name, transcript FROM interviews WHERE transcript LIKE "%bakery%" AND month = 7 AND day = 28 AND year = 2021;

    -- ouputs:
    --| Ruth    | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
    --| Eugene  | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
    --| Raymond | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket. |

-- Looking for cars that left the parking lot at the time frame specified by Ruth
    SELECT license_plate, activity FROM bakery_security_logs WHERE month = 7 AND day = 28 AND year = 2021 AND hour = 10 AND minute >= 15 AND minute <= 25;

    -- outputs:
    -- +---------------+----------+
    -- | license_plate | activity |
    -- +---------------+----------+
    -- | 5P2BI95       | exit     |
    -- | 94KL13X       | exit     |
    -- | 6P58WS2       | exit     |
    -- | 4328GD8       | exit     |
    -- | G412CB7       | exit     |
    -- | L93JTIZ       | exit     |
    -- | 322W7JE       | exit     |
    -- | 0NTHK55       | exit     |
    -- +---------------+----------+

-- Finding who Eugene saw withdrawing money on Leggett Street that drove off the parking lot:
    SELECT name FROM people WHERE id IN
        (SELECT person_id FROM bank_accounts WHERE account_number IN
            (SELECT account_number FROM atm_transactions WHERE month = 7 AND day = 28 AND year = 2021 AND atm_location = "Leggett Street" AND transaction_type = "withdraw"))
        AND license_plate IN
            (SELECT license_plate FROM bakery_security_logs WHERE month = 7 AND day = 28 AND year = 2021 AND hour = 10 AND minute >= 15 AND minute <= 25);

    -- output:
    -- +-------+
    -- | name  |
    -- +-------+
    -- | Iman  |
    -- | Luca  |
    -- | Diana |
    -- | Bruce |
    -- +-------+

-- Finding of those above who could have made the suspicious call:

    SELECT caller, receiver, duration FROM phone_calls WHERE caller IN
        (SELECT phone_number FROM people WHERE id IN
            (SELECT person_id FROM bank_accounts WHERE account_number IN
                (SELECT account_number FROM atm_transactions WHERE month = 7 AND day = 28 AND year = 2021 AND atm_location = "Leggett Street" AND transaction_type = "withdraw"))
            AND license_plate IN
                (SELECT license_plate FROM bakery_security_logs WHERE month = 7 AND day = 28 AND year = 2021 AND hour = 10 AND minute >= 15 AND minute <= 25))
        AND month = 7 AND day = 28 AND year = 2021 AND duration < 60;

        -- outputs:
        -- +----------------+----------------+----------+
        -- |     caller     |    receiver    | duration |
        -- +----------------+----------------+----------+
        -- | (367) 555-5533 | (375) 555-8161 | 45       |
        -- | (770) 555-1861 | (725) 555-3243 | 49       |
        -- +----------------+----------------+----------+

        -- so it must have been one of the callers above

-- finding passengers on the next day flights from Fiftyville who are among the suspicious callers:

    SELECT name, people.phone_number, passengers.flight_id FROM people, passengers
    WHERE people.passport_number = passengers.passport_number
    AND people.passport_number IN
        (SELECT passport_number FROM passengers WHERE flight_id IN
            (SELECT id FROM flights WHERE origin_airport_id IN
                (SELECT id FROM airports WHERE city = "Fiftyville") AND month = 7 AND day = 29 AND year = 2021 AND hour < 12))
    AND people.phone_number IN
        (SELECT caller FROM phone_calls WHERE caller IN
            (SELECT phone_number FROM people WHERE id IN
                (SELECT person_id FROM bank_accounts WHERE account_number IN
                    (SELECT account_number FROM atm_transactions WHERE month = 7 AND day = 28 AND year = 2021 AND atm_location = "Leggett Street" AND transaction_type = "withdraw"))
                AND license_plate IN
                    (SELECT license_plate FROM bakery_security_logs WHERE month = 7 AND day = 28 AND year = 2021 AND hour = 10 AND minute >= 15 AND minute <= 25))
            AND month = 7 AND day = 28 AND year = 2021 AND duration < 60)
    AND passengers.flight_id IN
        (SELECT id FROM flights WHERE origin_airport_id IN
                (SELECT id FROM airports WHERE city = "Fiftyville") AND month = 7 AND day = 29 AND year = 2021 AND hour < 12);

    -- output:
    -- +-------+----------------+-----------+
    -- | name  |  phone_number  | flight_id |
    -- +-------+----------------+-----------+
    -- | Bruce | (367) 555-5533 | 36        |
    -- +-------+----------------+-----------+

    -- So this indicates that Bruce is the thief, the accomplice was the owner of the phone (375) 555-8161 and
    -- the city the thief escaped for was the destination of flight 36.

    -- Following queries sum up the findings

    SELECT name FROM people WHERE phone_number = "(375) 555-8161";

    -- Outputs Robin, the accomplice.

    SELECT city FROM airports WHERE id = (SELECT destination_airport_id FROM flights WHERE id = 36);

    -- Outputs New York City, the thief's destination.
-- Keep a log of any SQL queries you execute as you solve the mystery.
.schema --to see the tables and columns

--get description from crime scene
select description from crime_scene_reports
where year = 2020 and month = 07 and day = 28
and street like 'Chamberlin%';

--get data from relevant interviews
select transcript, name, id from interviews
where year = 2020 and month = 07 and day = 28;

--get license plates based on lead from interview id:161
select license_plate from courthouse_security_logs
where year = 2020 and month = 07 and day = 28
and hour = 10 and minute > 14 and minute < 25
and activity = 'exit';

--get possible perp account number based on lead from interview id:162
select account_number from atm_transactions
where atm_location = 'Fifer Street'
and transaction_type = 'withdraw'
and year = 2020 and month = 07 and day = 28;

--get possible phone numbers suspect and accomplice based on interview id:163
select caller, receiver from phone_calls
where year = 2020 and month = 07 and day = 28
and duration < 60;

--get city suspects escaped to
select city from airports where id = (
select destination_airport_id from flights
where year = 2020 and month = 07 and day = 29
and origin_airport_id = (
select id from airports where city = 'Fiftyville')
order by hour, minute
limit 1
);

--get primary suspect's data by cross referencing all relevant leads
select distinct name, people.passport_number, people.id, people.phone_number from people

inner join phone_calls on people.phone_number in (
select caller from phone_calls
where year = 2020 and month = 07 and day = 28
and duration < 60)

inner join bank_accounts on people.id in (
select person_id from bank_accounts where account_number in(
select account_number from atm_transactions
where atm_location = 'Fifer Street'
and transaction_type = 'withdraw'
and year = 2020 and month = 07 and day = 28))

inner join courthouse_security_logs on people.license_plate in (
select license_plate from courthouse_security_logs
where year = 2020 and month = 07 and day = 28
and hour = 10 and minute > 14 and minute < 25
and activity = 'exit')

inner join passengers on people.passport_number in (
select passport_number from passengers where flight_id in (
select id from flights
where year = 2020 and month = 07 and day = 29
and origin_airport_id = (
select id from airports where city = 'Fiftyville')
order by hour, minute
limit 1
));

--get accomplice's name using the data we have
select name from people where phone_number = (
select receiver from phone_calls
where  day = 28 and year = 2020 and month = 07
and duration < 60 and caller = '(367) 555-5533');
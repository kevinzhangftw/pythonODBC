CREATE TRIGGER update_seats ON Booking AFTER INSERT 
AS
BEGIN
UPDATE Flight_Instance
SET available_seats = available_seats - (SELECT COUNT(*)
						FROM inserted
						WHERE 
Flight_Instance.flight_code = inserted.flight_code AND 
Flight_Instance.depart_date = inserted.depart_date)

FROM inserted
WHERE inserted.flight_code = Flight_Instance.flight_code 
	AND inserted.depart_date = Flight_Instance.depart_date
END

CREATE TRIGGER update_seats_d ON Booking AFTER DELETE 
AS
BEGIN
UPDATE Flight_Instance
SET available_seats = available_seats + (SELECT COUNT(*)
								FROM deleted
								WHERE Flight_Instance.flight_code = deleted.flight_code AND Flight_Instance.depart_date = deleted.depart_date)
FROM deleted
WHERE deleted.flight_code = Flight_Instance.flight_code 
	AND deleted.depart_date = Flight_Instance.depart_date
END


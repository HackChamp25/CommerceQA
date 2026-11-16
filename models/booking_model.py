from datetime import date

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Bookingdates(BaseModel):
    model_config = ConfigDict(extra="forbid")
    checkin: date
    checkout: date

    @model_validator(mode="after")
    def validate_booking_dates(self):
        if self.checkout <= self.checkin:
            raise ValueError("Check-out date must be after check-in date")
        return self

class Bookingrequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    firstname: str = Field(min_length=2, max_length=20)
    lastname: str = Field(min_length=2, max_length=20)
    totalprice: int = Field(ge=0)
    depositpaid: bool
    bookingdates: Bookingdates
    additionalneeds: str | None = None

class Bookingresponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: Bookingdates
    additionalneeds: str | None = None

class BookingCreateresponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    bookingid: int = Field(gt=0)
    booking: Bookingresponse

class BookingUpdaterequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    firstname: str | None = None
    lastname: str | None = None
    totalprice: int | None = None
    depositpaid: bool | None = None
    bookingdates: Bookingdates | None = None
    additionalneeds: str | None = None
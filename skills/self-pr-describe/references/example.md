# Example PR description

This example shows the tone, depth and structure to aim for. The product (a clinic booking app) is made up. Copy the shape, not the domain.

---

## Why

- **Late cancellations left clinics with an empty slot and no income.** A patient could cancel a 9:00 appointment at 8:55 and pay nothing, even though the clinic's policy charges a fee within 24 hours.
- **Patients weren't told about the fee before booking.** The policy appeared only on the clinic's website, so every dispute ended with the fee waived.

## What

- **Cancelling within 24 hours now charges the clinic's late-cancellation fee.** The fee is taken from the card saved at booking, and the patient gets a receipt by email.
- **Patients see the fee before they confirm.** The booking summary shows "Cancel free until" with the deadline, and the fee that applies after it.
- **Clinics set their own fee.** Settings → Policies → Late cancellation fee accepts A$0 to A$200. A$0 turns the fee off.
- **Existing bookings keep their old terms.** Only bookings made after this change can be charged.

| Situation | Before | After |
|---|---|---|
| Patient cancels 2 days ahead | Free | Free |
| Patient cancels 3 hours ahead | Free | Charged the clinic's fee (A$40 in the steps below) |
| Patient reviews the booking summary | Time and practitioner only | Adds the free-cancellation deadline and fee |
| Clinic fee set to A$0 | Free | Free, and no fee line is shown |

## How to manually test

1. **A late cancellation is charged**
   - As the clinic admin, open Settings → Policies → Late cancellation fee, enter A$40 and save.
   - As the patient, book an appointment starting 3 hours from now and pay with test card 4242 4242 4242 4242. The summary should show "Cancel free until" with a time that has already passed, and a A$40 fee.
   - Cancel it from My appointments. It should say "A$40 late-cancellation fee charged", and a receipt email should arrive.
   - Before: the cancellation went through with no charge.

2. **An early cancellation is free**
   - As the patient, book an appointment 3 days out, then cancel it straight away. It should cancel with no charge and no receipt.

3. **Existing bookings are never charged**
   - As the patient, cancel a booking made before this change was deployed, within 24 hours of its start. It should cancel with no charge.
   - As the clinic admin, set the fee back to A$0.

## Worth knowing

- **Every clinic starts with the fee turned off.** Existing clinics get A$0 until an admin enters an amount, so nothing changes for them on release.
- **A declined card doesn't block the cancellation.** The slot is freed and the fee is recorded as unpaid. There's no automatic retry yet; that's planned as a follow-up.

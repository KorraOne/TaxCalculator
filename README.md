# Personal Income Tax Estimator

## Overview
**Personal Income Tax Estimator** is a client-tax estimation system using **Pyro5** for remote database communication. It helps users calculate their tax return based on **biweekly income** and **tax withheld**.
The **Personal Income Tax Return Estimator** meant for a user to be able to estimate what their tax return will be
from their taxable income and their withheld tax.

The PITRE is made up of three sytems, the client, the server, and the database. These communicate using Pyro5.

## Features
Tax return calculation - Calculates income tax, medicare levy tax, and medicare levy surcharge
Input Data - Users can input their Fortnightly pay and withholding
Database Data - If the user has a TFN the system can find their taxable income and withholding automatically

## Tax Calculation Rates
The Personal Income Tax Estimator applies **progressive tax rates** based on the following brackets:
### **Australian Income Tax Rates (2024-25)**
| Taxable Income ($AUD) | Tax Rate (%) | Additional Tax |
|----------------------|-------------|----------------|
| $0 – $18,200       | 0%          | No tax payable |
| $18,201 – $45,000  | 19%         | $0 + 19% over $18,200 |
| $45,001 – $120,000 | 32.5%       | $5,092 + 32.5% over $45,000 |
| $120,001 – $180,000 | 37%         | $29,467 + 37% over $120,000 |
| Over $180,001      | 45%         | $51,667 + 45% over $180,000 |

### **Additional Considerations**
**Medicare Levy (2%)** – Applied to all taxable income 
**Private Health Insurance** – If a user has private health, 0% otherwise 1%-1.5%

## Installation & Setup
### Prerequisites
- Python 3.x  
- Pyro5 (`pip install Pyro5`)  
- pytest (for developers) 

### Steps to Run
1. **Download project**
   Locate project on your device

2. **Open Console at Project Location**
    In different consoles start
    a. Pyro     -```bash pyro5-ns```
    b. Database -```ash python server/database.py```
    c. Server   -```bash python server/server.py```
3. **Create a client**
    To make a client instance. Open a console in the project and run
    ```bash python client/mainClient.py```
    
1. **Start the Database Server**  
   ```bash
   python database.py
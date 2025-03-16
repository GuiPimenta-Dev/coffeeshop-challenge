# Project Overview

Welcome to the technical portion of our application process! We’re excited that you made it to this point and hope that you enjoy working on the upcoming Trio Challenge, a special take-home project that we designed to assess your technical maturity.

The Trio Challenge consists of creating a RESTful coffee shop order management application.

## Deliverables
- GitHub private repository with your solution.

## Instructions
1. Create a new empty private GitHub repository.
2. Develop and deliver a solution that is production-ready by opening a new PR in your repository.
3. Add `challenge@trio.dev` as a collaborator.
4. Record a video with your screen and camera walking through your solution.
5. Submit your project by answering all fields on [challenge.trio.dev](https://challenge.trio.dev).

You will have **7 days** to complete the project and return it. If you have any questions or are not sure about something, please contact `challenge@trio.dev`.

## Getting Started

This application needs to support two types of users: **Managers** and **Customers**. Each role has different permissions and responsibilities:

- **Managers** have full access to all features.
- **Customers** have limited access and cannot perform managerial actions.

To simulate role-based access, requests should include a `role` header with one of the following values:

```
role: customer
role: manager
```

🔹 **Note:** Authentication is not required for this challenge, only the role header is needed to differentiate users.


### **Managers**
Managers are responsible for overseeing order processing and ensuring smooth operations. Their main tasks include to change the status of an order:

- Orders can have one of the four statuses: **Waiting, Preparation, Ready, and Delivered**.
- Status transitions must follow one of this strict sequence:
  - **Waiting** → **Preparation** → **Ready** → **Delivered**

### Customers:
- Order and customize their orders with several options from the catalog below.

## Catalog with Pricing

| Product        | Base Price | Variation       | Price Change |
|---------------|------------|----------------|--------------|
| **Latte**     | $4.00      | Pumpkin Spice  | +$0.50       |
|               |            | Vanilla        | +$0.30       |
|               |            | Hazelnut       | +$0.40       |
| **Espresso**  | $2.50      | Single Shot    | +$0.00       |
|               |            | Double Shot    | +$1.00       |
| **Macchiato** | $4.00      | Caramel        | +$0.50       |
|               |            | Vanilla        | +$0.30       |
| **Iced Coffee** | $3.50    | Regular        | +$0.00       |
|               |            | Sweetened      | +$0.30       |
|               |            | Extra Ice      | +$0.20       |
| **Donuts**     | $2.00      | Glazed         | +$0.00       |
|               |            | Jelly          | +$0.30       |
|               |            | Boston Cream   | +$0.50       |

## Tasks

Your assignment is to build a complete, production-ready REST API for a coffee shop order management system. The application must include integration with external mock services to simulate real-world scenarios. Below are the detailed requirements for each endpoint:

### Required Endpoints

1. **View Menu** (`GET /menu`)
   - Must return a complete list of products with their base prices and all available variations
   - Response must include pricing details for each variation as shown in the catalog

2. **Place a New Order** (`POST /orders`)
   - Must accept a list of products with the variations
   - Must calculate the total price correctly based on base prices and variations
   - **Critical Requirement:** Integrate with the payment processing mock service
     ```http
     POST https://challenge.trio.dev/api/v1/payment?amount={TOTAL_AMOUNT}
     ```
   - Must display the complete payment service response in the terminal
   - Orders should ONLY be created if the payment service returns a successful response
   - All new orders must be created with the initial status of `Waiting`
   - The API should return appropriate error messages if payment fails

3. **View Order Details** (`GET /orders/{id}`)
   - Must return complete order information including:
     - All ordered items with their variations
     - Individual and total pricing
     - Current order status
     - Order creation timestamp

4. **Update Order Status** (`PATCH /orders/{id}/status`)
   - **Manager Only:** Endpoint must enforce role-based access (only managers can update status)
   - Must validate that status transitions follow the allowed sequence:
     - **Waiting** → **Preparation** → **Ready** → **Delivered**
   - **Critical Requirement:** Must integrate with the notification mock service after every successful status update
     ```http
     POST https://challenge.trio.dev/api/v1/notify?status={ORDER_STATUS}
     ```
   - Must display the complete notification service response in the terminal

# Evaluation

Present your solution using the language/framework of your choice, justifying your selection. 

What truly matters to us is your ability to analyze situations critically, justify your decisions, and clearly explain your reasoning.

**Feel free to leave comments in your code explaining your thought process and the rationale behind your choices.**  

### **Examples:**  

```python
# Given the simplicity of the use case, I chose to use X, Y, and Z.  
# However, in a production environment, A, B, or C might be a better choice.  

# This class is a simplified representation of X, Y, and Z.  
# In a production setting, we could consider a more robust approach, such as A, B, or C. 
```

<div align="right">
  <em>"Clean code always looks like it was written by someone who cares." - Michael Feathers</em>
</div>

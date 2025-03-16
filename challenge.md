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

- Orders can have one of five statuses: **Waiting, Preparation, Ready, Delivered, and Canceled**.
- Status transitions must follow one of this strict sequence:
  - **Waiting** → **Preparation** → **Ready** → **Delivered**

### Customers:
- Order and customize their orders with several options from the catalog below.
- A customer can cancel its own order if the order has status `Waiting`.
 - **Waiting** → **Canceled** 

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

Create the following **REST API endpoints**.
Any customer should be able to consume them using a **secure way**:

- **View Menu** (list of products with pricing)
- **Place a new order** (calculate the total price based on variations and process payment)
  - When placing an order, payment must be processed using the payment mock service:
  ```http
  GET https://challenge.trio.dev/api/v1/payment?amount={TOTAL_AMOUNT}
  ```
  - The response from the payment mock service should be logged to the terminal
  - Orders should only be created if payment is successful

- **View order details** (product list, pricing & order status)

- **Update Orders Status** (the response from the email mock service should be logged to the terminal)
- Customers must receive an email notification whenever their order status changes. To simulate this, use the following notification mock service:  

  ```http
  GET https://challenge.trio.dev/api/v1/notify?status={ORDER_STATUS}
  ```

  **Example:** Sending a notification for an order in the `Waiting` status:  
  [https://challenge.trio.dev/api/v1/notify?status=waiting](https://trio.challenge.com/api/v1/notify?status=waiting)  

  - The response from the notification mock service should be logged to the terminal

- **Cancel Orders** (only if it has `Waiting` status)

# Evaluation

Present your solution using the framework of your choice, justifying your selection. During the evaluation, we will discuss any missing aspects.

## What will be evaluated

- **Documentation**: Clear README with project description, setup instructions, and API documentation
- **Code Quality**: Small, focused functions with clear responsibilities and separation of business logic
- **Architecture**: Logical project structure with proper separation of layers and effective design patterns
- **Implementation**: Correct API endpoints with proper RESTful principles and status codes
- **Business Logic**: Accurate order processing, price calculations, and role-based authorization
- **Resilience**: Asynchronous processing and retry mechanisms for external service calls
- **Security**: Input validation and appropriate error handling
- **Testing**: Comprehensive test coverage with both unit and integration tests

## **What will be a differencial**

- Use of Docker for environment consistency.
- Implementation of design patterns for maintainable architecture.  
- Justification of design and implementation choices.  
- Proper component decoupling for modularity and flexibility.  

## **Use of AI in Development**  

We have no issue with the use of AI to assist in development—after all, it’s a tool we all use daily.  
However, what truly matters is your ability to **justify your decisions** and explain your reasoning.  

**Feel free to leave comments in your code explaining your thought process and the rationale behind your choices.**  

### **Examples:**  

```python
# Given the simplicity of this test case, I chose to use X, Y, and Z.  
# However, in a production environment, A, B, or C might be a better choice.  

# This class is a simplified representation of X, Y, and Z.  
# In a production setting, we could consider a more robust approach, such as A, B, or C. 

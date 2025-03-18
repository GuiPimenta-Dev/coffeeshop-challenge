import { Request, Response } from 'express';

import { OrderModel } from '../models/OrderModel';
import { Customer } from '../services/Customer';
import { Manager } from '../services/Manager';
import { Order } from '../services/Order';

export class OrderController {
	private Manager: Manager;
	private Order: Order;

	constructor() {
		this.Manager = new Manager();
		this.Order = new Order();
	}

	public async visualizeMenu(req: Request, res: Response): Promise<any> {
		try {
			const menu = Customer.visualizeMenu();
			return res.status(200).json(menu);
		} catch (error) {
			return res.status(500).json({ message: 'Error visualizing menu', error });
		}
	}

	public async placeOrder(req: Request, res: Response): Promise<any> {
		try {
			const { product, variation, userId } = req.body;
			console.log(req.body);
			const customer = new Customer(Number(userId));
			const newOrder = await customer.placeOrder(product, variation);
			return res.status(201).json(newOrder);
		} catch (error) {
			return res.status(500).json({ message: 'Error placing order', error });
		}
	}

	public async viewOrderDetails(req: Request, res: Response): Promise<any> {
		const { userId } = req.body;
		try {
			const customer = new Customer(userId);
			const orderDetails = await customer.viewOrderDetails();
			return res.status(200).json(orderDetails);
		} catch (error) {
			return res
				.status(500)
				.json({ message: 'Error viewing order details', error });
		}
	}

	public async updateOrderStatus(req: Request, res: Response): Promise<any> {
		try {
			const { orderId } = req.params;
			const manager = new Manager();
			const updatedOrder = await manager.updateOrderStatus(Number(orderId));
			return res.status(200).json(updatedOrder);
		} catch (error) {
			return res
				.status(500)
				.json({ message: 'Error updating order status', error });
		}
	}
}

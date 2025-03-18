import { productsMenu } from '../constants/productsMenu';
import { ORDER_STATUS } from '../enums/ORDER_STATUS';
import { UserModel } from '../models/UserModel';
import { Order } from './Order';

export class Customer {
	private userModel: UserModel;
	private orderService: Order;
	private customerId: number;

	constructor(customerId: number) {
		this.userModel = new UserModel();
		this.orderService = new Order();
		this.customerId = customerId;
		this.validateCustomerExists();
	}

	private async validateCustomerExists() {
		const user = await this.userModel.getUserById(this.customerId);
		if (!user) {
			throw new Error(`Customer with id ${this.customerId} does not exist.`);
		}
	}

	async placeOrder(product: string, variation: string) {
		const order = await this.orderService.createOrder(
			product,
			variation,
			this.customerId
		);
		return order;
	}

	viewOrderDetails() {
		return this.userModel.getOrdersByUserId(this.customerId);
	}

	static visualizeMenu(): typeof productsMenu {
		return productsMenu;
	}

	async cancelOrder(orderId: number) {
		const selectedOrder = await this.viewOrderDetails();

		if (selectedOrder[0].status !== ORDER_STATUS.waiting) {
			throw new Error("Order not in status of 'Waiting'");
		}
		return this.orderService.cancelOrder(orderId);
	}
}

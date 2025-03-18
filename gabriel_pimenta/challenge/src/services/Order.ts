import { STATUS_CODES } from 'http';
import { ORDER_STATUS } from '../enums/ORDER_STATUS';
import { orderInterface } from '../interface/orderInterface';
import { OrderModel } from '../models/OrderModel';
import { MenuService } from './MenuService';
import { NotificationService } from './NotificationService';

export class Order {
	private orderModel: OrderModel;
	private menuService: MenuService;
	private notificationService: NotificationService;

	constructor() {
		this.orderModel = new OrderModel();
		this.menuService = new MenuService();
		this.notificationService = new NotificationService();
	}

	async createOrder(product: string, variant: string, costumerId: number) {
		const price = this.menuService.calculatePrice(product, variant);
		const newOder: orderInterface = {
			product,
			variant,
			costumerId,
			status: ORDER_STATUS.waiting,
			price,
		};

		return await this.orderModel.createOrder(newOder);
	}

	async cancelOrder(orderId: number) {
		return this.orderModel.updateOrderStatus(orderId, ORDER_STATUS.canceled);
	}

	async getOrder(orderId: number) {
		const order = await this.orderModel.getOrder(orderId);
		if (!order) throw new Error('Order not found');
		return order[0];
	}

	async updateOrderStatus(orderId: number, newStatus: ORDER_STATUS) {
		const notificationResponse =
			await this.notificationService.sendNotification(newStatus);
		console.log('Notificação enviada:', notificationResponse);
		return this.orderModel.updateOrderStatus(orderId, newStatus);
	}

	async checkOrdersDetails() {}
}

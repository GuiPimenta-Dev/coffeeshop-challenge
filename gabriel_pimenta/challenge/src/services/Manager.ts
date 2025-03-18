import { ORDER_STATUS } from './../enums/ORDER_STATUS';

import { Order } from './Order';

export class Manager {
	private orderService: Order;

	constructor() {
		this.orderService = new Order();
	}

	async updateOrderStatus(orderId: number) {
		const order = await this.orderService.getOrder(orderId);

		const currentStatus = order.status;

		const statusArray: ORDER_STATUS[] = [
			ORDER_STATUS.waiting,
			ORDER_STATUS.preparation,
			ORDER_STATUS.ready,
			ORDER_STATUS.delivered,
		];
		const currentIndex = statusArray.indexOf(currentStatus);

		if (currentIndex === -1) {
			throw new Error(`Status not valid: ${currentStatus}`);
		}
		const nextStatus = statusArray[currentIndex + 1];
		if (!nextStatus) {
			throw new Error(`That status'${currentStatus}' is already the last one`);
		}

		const updatedOrder = await this.orderService.updateOrderStatus(
			orderId,
			nextStatus
		);
		return updatedOrder;
	}
}

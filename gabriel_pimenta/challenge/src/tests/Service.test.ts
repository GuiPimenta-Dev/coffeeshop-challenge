import { ORDER_STATUS } from '../enums/ORDER_STATUS';
import { OrderModel } from '../models/OrderModel';
import { Customer } from '../services/Customer';
import { Manager } from '../services/Manager';

describe('Application use cases test', () => {
	const orderModel = new OrderModel();
	it('Should visualize menu', () => {
		const menu = Customer.visualizeMenu();

		expect(menu[0].product).toBe('Latte');
		expect(menu[2].variation[0].price).toBe(0.5);
	});

	it('Should place a new order', async () => {
		const customer = new Customer(1);
		const newOrder = await customer.placeOrder('Espresso', 'Double Shot');

		expect(newOrder[0].product).toBe('Espresso');

		await orderModel.deleteOrder(newOrder[0].id);
	});

	it('Should view orders details', async () => {
		const customer = new Customer(1);

		const newOrder = await customer.placeOrder('Espresso', 'Double Shot');
		const ordersDetails = await customer.viewOrderDetails();

		expect(ordersDetails[0].product).toBe('Espresso');
		await orderModel.deleteOrder(newOrder[0].id);
	});

	it('Manager should be able to update the order status', async () => {
		const customer = new Customer(1);
		const manager = new Manager();

		const newOrder = await customer.placeOrder('Espresso', 'Double Shot');

		const updatedOrder = await manager.updateOrderStatus(newOrder[0].id);

		expect(updatedOrder[0].status).toBe(ORDER_STATUS.preparation);

		await orderModel.deleteOrder(newOrder[0].id);
	});
});

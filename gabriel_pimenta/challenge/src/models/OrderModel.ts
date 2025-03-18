import { db } from '../infra/database';
import { orderInterface } from '../interface/orderInterface';

export class OrderModel {
	getOrder(orderId: number) {
		return db.query('SELECT * FROM public.orders WHERE id = $1', orderId);
	}

	createOrder(order: orderInterface) {
		return db.query(
			'INSERT INTO public.orders (product, variation, price, status, customer_id) VALUES ($1, $2, $3, $4, $5) returning *',
			[
				order.product,
				order.variant,
				order.price,
				order.status,
				order.costumerId,
			]
		);
	}

	updateOrderStatus(orderId: number, status: string) {
		return db.query(
			'UPDATE public.orders SET status = $1 WHERE id = $2 RETURNING *',
			[status, orderId]
		);
	}

	deleteOrder(orderId: number) {
		return db.query('DELETE FROM public.orders WHERE id = $1 returning *', [
			orderId,
		]);
	}
}

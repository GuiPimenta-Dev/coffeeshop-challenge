import { USER_TYPES } from '../enums/USER_TYPES';
import { db } from '../infra/database';

export class UserModel {
	createUser(type: USER_TYPES) {
		return db.query(
			'INSERT INTO public.users (type) VALUES ($1) returning *',
			type
		);
	}

	getOrdersByUserId(userId: number) {
		return db.query(
			'SELECT o.id AS order_id, o.product, o.variation, o.price, o.status, o.data, o.customer_id AS customer_id FROM "orders" o JOIN "users" c ON o.customer_id = c.id WHERE c.id = $1;',
			userId
		);
	}

	getUserById(userId: number) {
		return db.query('SELECT * from public.users WHERE id = $1', userId);
	}

	deleteUserById(userId: number) {
		return db.query(
			'DELETE FROM public.users WHERE id = $1 RETURNING *',
			userId
		);
	}
}

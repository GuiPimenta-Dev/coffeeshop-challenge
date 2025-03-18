import axios from 'axios';
import { ORDER_STATUS } from '../enums/ORDER_STATUS';

export class NotificationService {
	// async sendNotification(status: ORDER_STATUS) {
	// 	try {
	// 		const response = await axios.post(
	// 			`https://challenge.trio.dev/api/v1/notify?status=${status}`
	// 		);
	// 		return response.data;
	// 	} catch (error: any) {
	// 		console.error(
	// 			'Erro ao enviar notificação:',
	// 			error.response?.data || error.message
	// 		);
	// 		throw new Error('Falha ao notificar serviço externo');
	// 	}
	// }
	async sendNotification(status: string): Promise<any> {
		const x = Math.floor(Math.random() * 5) + 1; // tempo aleatório entre 1 e 5 segundos
		const message = `The email was sent with the status ${status} after ${x} seconds`;

		return {
			statusCode: 200,
			body: JSON.stringify({
				success: true,
				message: message,
			}),
		};
	}
}

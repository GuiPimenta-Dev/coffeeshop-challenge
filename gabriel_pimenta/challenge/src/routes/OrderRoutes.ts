import express from 'express';
import { OrderController } from '../controllers/OrderController';
import authorize from '../middlewares/authorize';

const router = express.Router();
const orderController = new OrderController();

router.get(
	'/menu',
	authorize(['customer', 'manager']),
	orderController.visualizeMenu
);
router.post(
	'/order',
	authorize(['customer', 'manager']),
	orderController.placeOrder
);
router.get(
	'/orders',
	authorize(['customer', 'manager']),
	orderController.viewOrderDetails
);
router.put(
	'/order/status/:orderId',
	authorize(['manager']),
	orderController.updateOrderStatus
);

export default router;

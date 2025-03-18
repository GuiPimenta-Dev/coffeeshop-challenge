import express from 'express';
import orderRoutes from './routes/OrderRoutes';

const app = express();
app.use(express.json());

app.use('/api', orderRoutes);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
	console.log(`Servidor rodando na porta ${PORT}`);
});

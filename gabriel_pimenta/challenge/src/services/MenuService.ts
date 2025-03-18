import { productsMenu } from './../constants/productsMenu';

export class MenuService {
	private menu: typeof productsMenu;

	constructor() {
		this.menu = productsMenu;
	}

	private findProduct(product: string) {
		return this.menu.find((item) => item.product === product);
	}

	private findVariation(product: string, variation: string) {
		const foundProduct = this.findProduct(product);
		if (!foundProduct) {
			return null;
		}
		return foundProduct.variation.find((v) => v.name === variation);
	}

	calculatePrice(product: string, variation: string): number {
		const foundProduct = this.findProduct(product);
		if (!foundProduct) {
			throw new Error(`Erro: Produto "${product}" não encontrado.`);
		}

		const foundVariation = this.findVariation(product, variation);
		if (!foundVariation) {
			throw new Error(
				`Erro: A variação "${variation}" não existe para o produto "${product}".`
			);
		}

		return foundProduct.basePrice + foundVariation.price;
	}
}

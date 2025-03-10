import requests
import logging
from config import Config

logger = logging.getLogger(__name__)

class CoinExPayment:
    @staticmethod
    def create_invoice(amount: float, user_id: int):
        headers = {
            'Authorization': f'Bearer {Config.COINEX_API_KEY}',
            'Content-Type': 'application/json'
        }
        payload = {
            'amount': amount,
            'user_id': user_id,
            'currency': 'USD',
            'callback_url': 'https://your-domain.com/payment/callback'
        }
        
        try:
            response = requests.post(
                'https://api.coinex.com/v1/payment',
                json=payload,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Payment Error: {str(e)}")
            return None

    @staticmethod
    def verify_payment(payment_id: str):
        headers = {'Authorization': f'Bearer {Config.COINEX_API_KEY}'}
        try:
            response = requests.get(
                f'https://api.coinex.com/v1/payment/{payment_id}',
                headers=headers,
                timeout=5
            )
            return response.json().get('status') == 'paid'
        except requests.exceptions.RequestException:
            return False
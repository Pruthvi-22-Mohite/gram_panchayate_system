from django.core.management.base import BaseCommand
from modules.panchayat_budget.models import PanchayatBudget


class Command(BaseCommand):
    help = 'Seed the database with sample budget data'

    def handle(self, *args, **options):
        # Sample budget data
        sample_budgets = [
            {
                'budget_head': PanchayatBudget.HEALTH_INSPECTION,
                'previous_year_amount': 50000.00,
                'revenue_income': 15000.00,
                'revenue_collection': 20000.00,
                'expenditure_allotted': 30000.00,
                'expenditure_spent': 25000.00,
            },
            {
                'budget_head': PanchayatBudget.ELECTRICITY_TAX,
                'previous_year_amount': 120000.00,
                'revenue_income': 25000.00,
                'revenue_collection': 30000.00,
                'expenditure_allotted': 40000.00,
                'expenditure_spent': 35000.00,
            },
            {
                'budget_head': PanchayatBudget.GARBAGE_TAX,
                'previous_year_amount': 80000.00,
                'revenue_income': 10000.00,
                'revenue_collection': 15000.00,
                'expenditure_allotted': 20000.00,
                'expenditure_spent': 18000.00,
            },
            {
                'budget_head': PanchayatBudget.PUBLIC_WATER_SUPPLY,
                'previous_year_amount': 200000.00,
                'revenue_income': 30000.00,
                'revenue_collection': 25000.00,
                'expenditure_allotted': 50000.00,
                'expenditure_spent': 45000.00,
            },
            {
                'budget_head': PanchayatBudget.OLD_PRODUCT_INCOME,
                'previous_year_amount': 75000.00,
                'revenue_income': 5000.00,
                'revenue_collection': 10000.00,
                'expenditure_allotted': 15000.00,
                'expenditure_spent': 12000.00,
            }
        ]

        # Create budget entries
        for budget_data in sample_budgets:
            budget = PanchayatBudget(**budget_data)
            budget.save()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created budget entry: {budget.budget_head}')
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded all budget data')
        )
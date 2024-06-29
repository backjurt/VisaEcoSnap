import os
import pandas as pd
import openai
import numpy as np

client = openai.OpenAI(api_key = os.getenv("OPENAI_API_KEY"))


def load_data(file_path):
    excel_data = pd.ExcelFile(file_path)
    card_data_df = pd.read_excel(excel_data, sheet_name='2_Card data')
    open_banking_data_df = pd.read_excel(excel_data, sheet_name='3_Open banking data')
    return card_data_df, open_banking_data_df

def data_analysis(open_banking_data_df):
    account_ids = open_banking_data_df["Value.accountId"].unique()
    segments = open_banking_data_df["mrch_catg_rlup_nm2"].unique()
    recommerce_segments_set = {
        'ART DEALERS & GALLERIES', 'ARTIST/CRAFT SHOPS', 'BOOK STORES',
        'COMPUTER SOFTWARE STORES', 'ELECTRONICS STORES', 'GIFT, CARD, NOVELTY STORES',
        'JEWELRY STORES', 'MISC APPAREL/ACCESS STORES', 'MISC SPECIALTY RETAIL',
        'RECORD STORES', 'SPORTING GOODS STORES', 'STATIONERY STORES', 'VARIETY STORES',
        'WOMENS READY TO WEAR STORES'
    }

    mean_segment_spends = {
        account_id: {
            segment: mean
            for segment, mean in {
                segment: open_banking_data_df[
                    (open_banking_data_df["Value.accountId"] == account_id) & 
                    (open_banking_data_df["mrch_catg_rlup_nm2"] == segment)
                ]["amount"].mean()
                for segment in segments
            }.items()
            if not np.isnan(mean)
        }
        for account_id in account_ids
    }

    mean_recommerce_segment_spends = {
        account_id: {
            segment: mean
            for segment, mean in {
                segment: open_banking_data_df[
                    (open_banking_data_df["Value.accountId"] == account_id) & 
                    (open_banking_data_df["mrch_catg_rlup_nm2"] == segment)
                ]["amount"].mean()
                for segment in segments if segment in recommerce_segments_set
            }.items()
            if not np.isnan(mean)
        }
        for account_id in account_ids
    }

    common_segments = set(segments)
    for account_id in account_ids:
        account_segments = set(mean_segment_spends[account_id].keys())
        common_segments.intersection_update(account_segments)

    mean_common_segment_spends = {
        account_id: {
            segment: mean
            for segment, mean in {
                segment: open_banking_data_df[
                    (open_banking_data_df["Value.accountId"] == account_id) & 
                    (open_banking_data_df["mrch_catg_rlup_nm2"] == segment)
                ]["amount"].mean()
                for segment in common_segments
            }.items()
            if not np.isnan(mean)
        }
        for account_id in account_ids
    }

    sum_segment_spends = {
        account_id: {
            segment: total
            for segment, total in {
                segment: open_banking_data_df[
                    (open_banking_data_df["Value.accountId"] == account_id) & 
                    (open_banking_data_df["mrch_catg_rlup_nm2"] == segment)
                ]["amount"].sum()
                for segment in segments
            }.items()
            if not np.isnan(total)
        }
        for account_id in account_ids
    }

    sum_recommerce_segment_spends = {
        account_id: {
            segment: total
            for segment, total in {
                segment: open_banking_data_df[
                    (open_banking_data_df["Value.accountId"] == account_id) & 
                    (open_banking_data_df["mrch_catg_rlup_nm2"] == segment)
                ]["amount"].sum()
                for segment in segments if segment in recommerce_segments_set
            }.items()
            if not np.isnan(total)
        }
        for account_id in account_ids
    }

    sum_common_segment_spends = {
        account_id: {
            segment: total
            for segment, total in {
                segment: open_banking_data_df[
                    (open_banking_data_df["Value.accountId"] == account_id) & 
                    (open_banking_data_df["mrch_catg_rlup_nm2"] == segment)
                ]["amount"].sum()
                for segment in common_segments
            }.items()
            if not np.isnan(total)
        }
        for account_id in account_ids
    }

    count_segment_spends = {
        account_id: {
            segment: count
            for segment, count in {
                segment: open_banking_data_df[
                    (open_banking_data_df["Value.accountId"] == account_id) & 
                    (open_banking_data_df["mrch_catg_rlup_nm2"] == segment)
                ]["amount"].count()
                for segment in segments
            }.items()
            if not np.isnan(count)
        }
        for account_id in account_ids
    }

    count_recommerce_segment_spends = {
        account_id: {
            segment: count
            for segment, count in {
                segment: open_banking_data_df[
                    (open_banking_data_df["Value.accountId"] == account_id) & 
                    (open_banking_data_df["mrch_catg_rlup_nm2"] == segment)
                ]["amount"].count()
                for segment in recommerce_segments_set
            }.items()
            if not np.isnan(count)
        }
        for account_id in account_ids
    }

    count_common_segment_spends = {
        account_id: {
            segment: count
            for segment, count in {
                segment: open_banking_data_df[
                    (open_banking_data_df["Value.accountId"] == account_id) & 
                    (open_banking_data_df["mrch_catg_rlup_nm2"] == segment)
                ]["amount"].count()
                for segment in common_segments
            }.items()
            if not np.isnan(count)
        }
        for account_id in account_ids
    }

    total_spend = sum(
        sum_segment_spends[account_id][segment]
        for account_id in account_ids
        for segment in segments
    )

    total_transactions = sum(
        count_segment_spends[account_id][segment]
        for account_id in account_ids
        for segment in segments
    )

    # Rank accounts by their total spend
    total_spends_by_account = {
        account_id: sum(
            sum_segment_spends[account_id][segment]
            for segment in segments
        )
        for account_id in account_ids
    }

    rank_total_spends = {
        account_id: rank
        for rank, (account_id, _) in enumerate(
            sorted(total_spends_by_account.items(), key=lambda item: item[1]), 1
        )
    }

    # Rank accounts by their spend in each common segment
    rank_common_segment_spends = {
        segment: sorted(
            [
                (account_id, sum_segment_spends[account_id].get(segment, 0))
                for account_id in account_ids
            ],
            key=lambda x: x[1]
        )
        for segment in common_segments
    }

    average_spends_per_segment = {
        segment: np.mean([
            sum_segment_spends[account_id].get(segment, 0)
            for account_id in account_ids
        ])
        for segment in segments
    }

    summary = {
        "mean segment spends": mean_segment_spends,
        "mean recommerce segment spends": mean_recommerce_segment_spends,
        "mean common segment spends": mean_common_segment_spends,
        "sum segment spends": sum_segment_spends,
        "sum recommerce segment spends": sum_recommerce_segment_spends,
        "sum common segment spends": sum_common_segment_spends,
        "count segment spends": count_segment_spends,
        "count recommerce segment spends": count_recommerce_segment_spends,
        "count common segment spends": count_common_segment_spends,
        "total spend": total_spend,
        "total transactions": total_transactions,
        "rank total spends": rank_total_spends,
        "rank common segment spends": rank_common_segment_spends,
        "average spends per segment": average_spends_per_segment
    }

    return summary

def generate_financial_summary(summary, account_id):
    total_spend_account = sum(summary['sum segment spends'][account_id].values())
    total_transactions_account = sum(summary['count segment spends'][account_id].values())

    financial_summary = f"""
    🎉 **Financial Snapshot** 📊

    Wow! You have done an incredible job managing your finances this month! Here's a snapshot of your financial journey:

    💸 Total Spending: £{total_spend_account:.2f} across {total_transactions_account} transactions

    Here's a breakdown of your spending:
    """
    
    for segment, total in summary['sum segment spends'][account_id].items():
        average_spend = summary['average spends per segment'][segment]
        comparison = total - average_spend
        if comparison < 0:
            comparison_text = f"£{abs(comparison):.2f} less than the average spender. Great job saving!"
        else:
            comparison_text = f"£{abs(comparison):.2f} more than the average spender. Reflect on this spending."
        financial_summary += f"\n    - **{segment}**: £{total:.2f} ({comparison_text})"

    financial_summary += "\n\nYour engagement in recommerce activities:"
    for segment, total in summary['sum recommerce segment spends'][account_id].items():
        financial_summary += f"\n    - **{segment}**: £{total:.2f}"

    financial_summary += "\n\nComparisons with other spenders:"

    rank_total = summary['rank total spends'][account_id]
    total_accounts = len(summary['rank total spends'])
    financial_summary += f"\n    - You are ranked {rank_total} out of {total_accounts} accounts in total spending."

    for segment in summary['rank common segment spends']:
        ranks = summary['rank common segment spends'][segment]
        user_rank = next((rank for rank, (acc_id, _) in enumerate(ranks, 1) if acc_id == account_id), None)
        if user_rank is not None:
            percent_rank = (user_rank / total_accounts) * 100
            financial_summary += f"\n    - In **{segment}**, you are ranked {user_rank} out of {total_accounts} accounts (top {percent_rank:.2f}%)."

    return financial_summary

# Using OpenAI to enhance the text
def openai_summary(financial_summary_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a creative financial assistant that generates monthly summaries of people's financial data in a Spotify wrapped style.\
            You do not make the summary music themed but you like using emojis. Keep it punchy and entertaining."},
            {"role": "user", "content": f"Generate an engaging and personalized financial summary based on the following data:\n{financial_summary_text} \
            Make the user feel that they are savvy and celebrating their individuality."}
        ],
        max_tokens=500
    )

    enhanced_summary_text = response.choices[0].message.content.strip()
    print(enhanced_summary_text)

def main():
    working_directory = 'REPLACE_WITH_YOUR_WORKING_DIRECTORY'
    file_name = 'Visa Climate Tech Data.xlsx'
    file_path = os.path.join(working_directory, file_name)
    card_data_df, open_banking_data_df = load_data(file_path)
    summary = data_analysis(open_banking_data_df)
    financial_summary_text = generate_financial_summary(summary, account_id='94177e7a3daa4ef18746b355980ebd5f')
    enhanced_summary_text = openai_summary(financial_summary_text)
    return enhanced_summary_text

main()

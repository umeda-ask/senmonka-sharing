from . import views_const

# ジャンル検索用大カテゴリ参照関数

def category_check(category_type:str, category_number:int) -> str:

# category_typeで、大カテゴリを参照したいのか、小カテゴリを参照したいのか確認
# その後、category_numberで指定した番号のviews_constの定数を参照する

    if category_type ==  "primary" :
        if category_number == 1:
            return views_const.primary_category_number_1

        elif category_number == 2:
            return views_const.primary_category_number_2

        elif category_number == 3:
            return views_const.primary_category_number_3

        elif category_number == 4:
            return views_const.primary_category_number_4

        else:
            return "category_numberが不正です"

    elif category_type == "sub" :
        pass

    else:
        return "category_typeが不正です"

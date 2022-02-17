import plotly.express as px
from app import app

def groupbygenderbar(ref_df, metric, aggfunc):
    if aggfunc == 'count':
        bar = px.bar(ref_df.groupby(['Sex', 'Age_Group'])[metric].count().reset_index(),
                     y=metric,
                     x='Age_Group',
                     color='Sex',
                     text=metric
                     )
    elif aggfunc == 'average':
        bar = px.bar(ref_df.groupby(['Sex', 'Age_Group'])[metric].mean().round(2).reset_index(),
                     y=metric,
                     x='Age_Group',
                     color='Sex',
                     text=metric,
                     barmode='group'
                     )

    return bar


def groupbyclassbar(ref_df, metric, aggfunc):
    if aggfunc == 'count':
        bar = px.bar(ref_df.groupby(['Class', 'Age_Group'])[metric].count().reset_index(),
                     y=metric,
                     x='Age_Group',
                     color='Class',
                     text=metric
                     )
    elif aggfunc == 'average':
        bar = px.bar(ref_df.groupby(['Class', 'Age_Group'])[metric].mean().round(2).reset_index(),
                     y=metric,
                     x='Age_Group',
                     color='Class',
                     text=metric,
                     barmode='group'
                     )

    bar.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)'})

    return bar

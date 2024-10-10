import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')


#functions
def print_table(title,data):
    st.write(title)
    st.write(data)
    
def languages_in_repos_visual(data):
    top_languages_chart_over_repos = px.bar(
        data,
        x='count',
        y='languages',
        orientation='h',
        labels={'x':'number of Repositories',
                'y':'languages'},
        title='Top 10 programing languages used in most Repositroies',
        category_orders={'languages': data['languages'].tolist()})
    st.plotly_chart(top_languages_chart_over_repos)

def most_used_languages_ppl_visual(data):
    top_languages_charts_over_ppl= px.bar(
        data,
        x='contributors',
        y='language',
        orientation='h',
        labels={'x':'number of people used', 'y':'languages'},
        title='Top 10 languages used by most of the people',
        category_orders={'language': data['language'].tolist()})
    st.plotly_chart(top_languages_charts_over_ppl)
    
    
def most_liked_repos_visual(data):
    top_likes_charts= px.bar(data, x='repositories', y='stars_count', labels={'x':'repositories', 'y':'number of likes'}, title='Top 10 repositories liked by most of the people')
    st.plotly_chart(top_likes_charts)


def most_ppl_contributed_repos_visual(data):
    top_contributors_chart = px.bar(data, x='repositories', y='contributors', labels={'x':'repositories', 'y':'number of contibutors'}, title='Top 10 repositories for most people contributed')
    st.plotly_chart(top_contributors_chart)

def most_issues_repositories(data):
    top_issues_chart = px.bar(data, x='repositories', y='issues_count', labels={'x':'repositories', 'y':'number of issues'}, title='Top 10 repositories with having most issues');
    st.plotly_chart(top_issues_chart)
    
def forks_vs_pulls(data):
    fork_vs_pull_plot = px.scatter(data, x='forks_count', y='pull_requests',
                     title='Scatter Plot of Forks vs. Pull Requests',
                     hover_name='repositories')
    st.plotly_chart(fork_vs_pull_plot)
    
def contributors_vs_issues_lines(data):
    contributors_vs_issues_line = px.line(
        data,
        x='contributors', 
        y='issues_count',
        title='Line Chart of Contributors vs. Issues',
        labels={'Contributors': 'Number of Contributors', 'Issues': 'Number of Issues'},
    )
    st.plotly_chart(contributors_vs_issues_line )


st.set_page_config(page_title='sample',page_icon=':bar_chart:',layout='wide')
#st.markdown('<style> section{background-color:white;}</style>',unsafe_allow_html=True)

df=pd.read_csv('dataset/github_dataset.csv',encoding='ISO-8859-1')
st.write(df.head(5))
    
#side bar
st.sidebar.header('CHOOSE YOUR FILTER')
dataKind=st.sidebar.selectbox('pick your type',['pick your type','top heighlets','correlations'])
selected=None
choose_formate=None
formate=None
if dataKind!='pick your type':
    choose_formate=st.sidebar.selectbox('choose kind of visualaisation',['pick your type','table formate','vizualaisation fromate','both formates'])
if choose_formate and choose_formate!='pick your type':
    if dataKind=='top heighlets':
        formate=st.sidebar.selectbox(
            'pick your type',
            ['pick your type',
             'most used languages in repos top 15',
             'most used languages by people top 15',
             'most liked repositories top 15',
             'most people contributed project top 15',
             'top 15 repositroies having more issues'
             
             ])
    else:
        formate=st.sidebar.selectbox(
            'pick your types',
            ['pick your type',
             'forks vs pull request',
             'contributors vs issues'
             ]
            )
if formate and formate!='pick your type' and dataKind=='top heighlets':
    # making horizontal barchats for the top 15 languages used in most of the repositroies
    if formate=='most used languages in repos top 15':
        top_languages_over_repos=df['language'].value_counts().reset_index()
        top_languages_over_repos.columns=['languages','count']
        top_languages_over_repos=top_languages_over_repos.sort_values(by='count',ascending=False,inplace=False)
        if choose_formate=='table formate':
            print_table('most used languages in repositries',top_languages_over_repos.head(15))
        elif choose_formate=='vizualaisation fromate':
            languages_in_repos_visual(top_languages_over_repos.head(15))
        else:
            print_table('most used languages in repositries',top_languages_over_repos.head(15))
            languages_in_repos_visual(top_languages_over_repos.head(15))
            
     #making  horizontal barchats for the top 15 languages used by the most people       
    elif formate=='most used languages by people top 15':
        top_languages_over_ppl=df.groupby('language')['contributors'].sum().reset_index()
        top_languages_over_ppl=top_languages_over_ppl[['language','contributors']]
        top_languages_over_ppl=top_languages_over_ppl.sort_values(by='contributors',ascending=False,inplace=False)
        if choose_formate=='table formate':
            print_table('most used languages by people top 15',top_languages_over_ppl.head(15))
        elif choose_formate=='vizualaisation fromate':
            most_used_languages_ppl_visual(top_languages_over_ppl.head(15))
        else:
            print_table('most used languages by people top 15',top_languages_over_ppl.head(15)) 
            most_used_languages_ppl_visual(top_languages_over_ppl.head(15))
            
    #making vartical barcharts for the top15 most liked repositories
    elif formate=='most liked repositories top 15':
        top_stars_count=df.sort_values(by='stars_count',ascending=False,inplace=False)
        top_stars_count=top_stars_count[['repositories','stars_count']]
        if choose_formate=='table formate':
            print_table('most liked repositories',top_stars_count.head(15))
        elif choose_formate=='vizualaisation formate':
            most_liked_repos_visual(top_stars_count.head(15))
        else:
            print_table('most liked repositories',top_stars_count.head(15))
            most_liked_repos_visual(top_stars_count.head(15))
            
    #makig vertical barcharts for the top 15 most contributed repositories
    elif formate=='most people contributed project top 15':
        top_contributors=df[['repositories','contributors']]
        top_contributors=top_contributors.sort_values(by='contributors',ascending=False,inplace=False)
        if choose_formate=='table formate':
            print_table('most people contributed project top 15',top_contributors.head(15))
        elif choose_formate=='vizualisation formate':
            most_ppl_contributed_repos_visual(top_contributors.head(15))
        else:
            print_table('most people contributed project top 15',top_contributors.head(15))
            most_ppl_contributed_repos_visual(top_contributors.head(15))
    # making vertival barcharts for the top 15 repositories having most issues
    else:
        top_issues=df[['repositories','issues_count']]
        top_issues=top_issues.sort_values(by='issues_count',ascending=False,inplace=False)
        if choose_formate=='table formate':
            print_table('top 15 repositroies having more issues',top_issues.head(15))
        elif choose_formate=='vizualisation formate':
            most_issues_repositories(top_issues.head(15))
        else:
           print_table('top 15 repositroies having more issues',top_issues.head(15)) 
           most_issues_repositories(top_issues.head(15))
if formate and formate!='pick your type' and dataKind=='correlations':
    
#making scatter plot between forks and pullrequests
    if formate=='forks vs pull request':
        fork_vs_pull=df[['forks_count','pull_requests','repositories']]
        if choose_formate=='table formate':
            print_table('forks vs pull requests correlation',fork_vs_pull.head(30))
        elif choose_formate=='vizualisation formate':
            forks_vs_pulls(fork_vs_pull)
        else:
            print_table('forks vs pull requests correlation',fork_vs_pull.head(30))
            forks_vs_pulls(fork_vs_pull)
    else:
        contributors_vs_issues=df[['contributors','issues_count']]
        contributors_vs_issues=contributors_vs_issues.sort_values(by='contributors',ascending=False,inplace=False)
        print(choose_formate)
        if choose_formate=='table formate':
            print_table('contributors and correlation',contributors_vs_issues)
        elif choose_formate=='vizualaisation fromate':
            contributors_vs_issues_lines(contributors_vs_issues)
        else:
           print_table('contributors and correlation',contributors_vs_issues) 
           contributors_vs_issues_lines(contributors_vs_issues) 
        
        
            
           
        





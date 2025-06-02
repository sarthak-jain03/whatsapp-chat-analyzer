from urlextract import URLExtract
extractor = URLExtract()
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Fetching total number of messages
    num_messages = df.shape[0]

    # Fetching total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
        
    # Fetching total number of media messages shared
    media_messages_shared = df[df['message'] == '<Media omitted>\n'].shape[0]

    # Fetching total number of links shared
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), media_messages_shared, len(links)


# Fetching most busy users
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0] * 100), 2).reset_index().rename(
        columns={'user': 'name', 'count': 'percent'})
    return x, df


# Generating wordCloud
def create_wordCloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'Notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    wc = WordCloud(width=500, height=500, background_color='black')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


# Most common words
def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'Notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    f = open(r'stop_hinglish.txt')
    stop_words = f.read()

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    common_words_df = pd.DataFrame(Counter(words).most_common(20))
    return common_words_df


# Emojis and their count
def emojis_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emojis_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emojis_df

# Monthly timeline
def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

# Daily Timeline
def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

# Weekly Activity
def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

# Monthly Activity Map
def monthly_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

# Activity Heat Map
def activity_heat_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_activity = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_activity


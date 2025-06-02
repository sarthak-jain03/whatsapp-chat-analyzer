import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = preprocessor.preprocess(data)
    # st.dataframe(df)
    
    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('Notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
    if st.sidebar.button('Show Analysis'):

        st.title("Top Statistics")
        num_messages, words, media_messages_shared, links_shared = helper.fetch_stats(selected_user, df)


        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total Msgs')
            st.title(num_messages)

        with col2:
            st.header('Total Words')
            st.title(words)

        with col3:
            st.header('Media Shared')
            st.title(media_messages_shared)

        with col4:
            st.header('Links Shared')
            st.title(links_shared)


        # Monthly Timeline
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # Daily Timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # Activity Map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header('Most Busy Day')
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='blue')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header('Most Busy Month')
            busy_month = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        # Activity Heap Map
        st.title('Weekly Activity Map')
        user_activity = helper.activity_heat_map(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_activity)
        plt.yticks(rotation='horizontal')
        st.pyplot(fig)



        # finding the most busy users in the group (group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)


        # Generating wordCloud
        st.title('WordCloud')
        df_wc = helper.create_wordCloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        # Most common words
        common_words_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(common_words_df[0], common_words_df[1], color='green')
        # plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

        # Emojis Analysis
        emojis_df = helper.emojis_helper(selected_user,df)
        st.title('Emoji Analysis')
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emojis_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emojis_df[1].head(),labels=emojis_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)















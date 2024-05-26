from cassandra.cluster import Cluster
from datetime import datetime, timedelta
from collections import defaultdict

from src.cassandra_config import CASSANDRA_KEYSPACE, CASSANDRA_HOSTS

def connect_to_cassandra():
    cluster = Cluster(['cassandra'])
    session = cluster.connect(CASSANDRA_KEYSPACE)
    return cluster, session

def get_last_n_hours(n: int):
    cluster, session = connect_to_cassandra()
    
    end_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    start_time = end_time - timedelta(hours=n)
    
    results = defaultdict(lambda: {'time_start': '', 'time_end': '', 'statistics': []})
    
    current_start = start_time
    while current_start < end_time:
        current_end = current_start + timedelta(hours=1)
        
        query = """
        SELECT hour_start, hour_end, domain, page_count
        FROM hourly_stats
        WHERE hour_start = %s 
        allow filtering
        """
        rows = session.execute(query, (current_start,))
        
        for row in rows:
            time_key = row.hour_start.strftime("%Y-%m-%d %H:%M")
            if not results[time_key]['time_start']:
                results[time_key]['time_start'] = row.hour_start.strftime("%Y-%m-%d %H:%M")
                results[time_key]['time_end'] = row.hour_end.strftime("%Y-%m-%d %H:%M")
            
            results[time_key]['statistics'].append({row.domain: row.page_count})
        
        current_start = current_end
    
    cluster.shutdown()
    return list(results.values())

def get_last_n_hours_by_bots(n: int):
    cluster, session = connect_to_cassandra()
    
    end_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    start_time = end_time - timedelta(hours=n)
    
    result = {
        'time_start': start_time.strftime("%Y-%m-%d %H:%M"),
        'time_end': end_time.strftime("%Y-%m-%d %H:%M"),
        'statistics': []
    }
    
    domain_bot_counts = defaultdict(int)
    
    current_start = start_time
    while current_start < end_time:
        current_end = current_start + timedelta(hours=1)
        
        query = """
        SELECT time_start, time_end, domain, created_by_bots
        FROM bot_stats
        WHERE time_start = %s
        allow filtering
        """
        rows = session.execute(query, (current_start,))
        
        for row in rows:
            domain_bot_counts[row.domain] += row.created_by_bots
        
        current_start = current_end
    
    for domain, bot_count in domain_bot_counts.items():
        result['statistics'].append({'domain': domain, 'created_by_bots': bot_count})
    
    cluster.shutdown()
    return result

def get_top_users(n: int):
    cluster, session = connect_to_cassandra()
    
    end_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    start_time = end_time - timedelta(hours=n)
    
    user_counts = defaultdict(lambda: {'user_name': '', 'pages': []})
    
    current_start = start_time
    while current_start < end_time:
        current_end = current_start + timedelta(hours=1)
        
        query = """
        SELECT user_id, user_name, page_title, creation_time
        FROM user_stats
        WHERE creation_time >= %s AND creation_time < %s
        ALLOW FILTERING
        """
        rows = session.execute(query, (current_start, current_end))
        
        for row in rows:
            if not user_counts[row.user_id]['user_name']:
                user_counts[row.user_id]['user_name'] = row.user_name
            
            user_counts[row.user_id]['pages'].append(row.page_title)
        
        current_start = current_end
    
    top_users = sorted(user_counts.items(), key=lambda x: len(x[1]['pages']), reverse=True)[:20]
    
    result = {
        'time_start': start_time.strftime("%Y-%m-%d %H:%M"),
        'time_end': end_time.strftime("%Y-%m-%d %H:%M"),
        'statistics': []
    }
    
    for user_id, data in top_users:
        result['statistics'].append({
            'user_id': user_id,
            'user_name': data['user_name'],
            'page_titles': data['pages'],
            'page_count': len(data['pages'])
        })
    
    cluster.shutdown()
    return result


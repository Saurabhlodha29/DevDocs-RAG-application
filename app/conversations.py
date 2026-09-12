# This file acts as the data access layer from the Supabase Database for the conversation metadata

from vector_store import supabase

def create_conversation(thread_id : str, title : str):
    response = (
        supabase.table('conversations')
        .insert({
            'thread_id':thread_id,
            'title':title
        }).execute()
    )
    
    return response.data

def get_conversations():
    response = (
        supabase.table('conversations')
        .select('*')
        .order('updated_at',desc = True)
        .execute()
    )
    
    return response.data

def get_single_conversation(thread_id : str):
    response = (
        supabase.table('conversations')
        .select('*')
        .eq('thread_id',thread_id)
        .single()
        .execute()
    )
    
    return response.data

def update_conversation(thread_id : str, title : str):
    response = (
        supabase.table('conversations')
        .update({
            'title':title,
            'updated_at':"now()"
        })
        .eq('thread_id',thread_id)
        .execute()
    )
    
    return response.data

def conversation_exists(thread_id : str):
    response = (
        supabase.table('conversations')
        .select('thread_id')
        .eq('thread_id',thread_id)
        .execute()
    )
    
    return len(response.data) > 0
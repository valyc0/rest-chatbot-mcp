#!/usr/bin/env python3
"""
Test script per le API di gestione della memoria delle conversazioni
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

async def test_memory_apis():
    """Test completo delle API di memoria"""
    
    async with aiohttp.ClientSession() as session:
        
        print("🧪 Test delle API di gestione memoria conversazioni")
        print("=" * 60)
        
        # 1. Controllo stato del server
        print("\n1. 📊 Controllo stato server...")
        try:
            async with session.get(f"{BASE_URL}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Server attivo - Status: {data['status']}")
                else:
                    print(f"❌ Server non raggiungibile - Status: {response.status}")
                    return
        except Exception as e:
            print(f"❌ Errore connessione server: {e}")
            return
        
        # 2. Statistiche memoria iniziali
        print("\n2. 📈 Statistiche memoria iniziali...")
        try:
            async with session.get(f"{BASE_URL}/api/v1/memory/stats") as response:
                if response.status == 200:
                    stats = await response.json()
                    print(f"✅ Memoria limite: {stats['memory_limit']} messaggi")
                    print(f"✅ Utenti attivi: {stats['active_users']}")
                    print(f"✅ User ID default: {stats['default_user_id']}")
                    if stats['users']:
                        for user_id, user_stats in stats['users'].items():
                            print(f"   - Utente {user_id}: {user_stats['message_count']} messaggi")
                    initial_users = stats['active_users']
                else:
                    print(f"❌ Errore nel recupero statistiche: {response.status}")
                    return
        except Exception as e:
            print(f"❌ Errore statistiche: {e}")
            return
        
        # 3. Creiamo alcune conversazioni di test
        print("\n3. 💬 Creazione conversazioni di test...")
        test_queries = [
            {"user_id": "user1", "prompt": "Ciao, come stai?"},
            {"user_id": "user1", "prompt": "Dimmi qualcosa sui database"},
            {"user_id": "user2", "prompt": "Che tempo fa oggi?"},
            {"user_id": "user2", "prompt": "Spiegami Python"},
        ]
        
        for i, query in enumerate(test_queries, 1):
            try:
                async with session.post(f"{BASE_URL}/api/v1/query", json=query) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"✅ Query {i} ({query['user_id']}): {data['response'][:50]}...")
                    else:
                        print(f"❌ Errore query {i}: {response.status}")
            except Exception as e:
                print(f"❌ Errore nella query {i}: {e}")
                
        # Piccola pausa per permettere il salvataggio
        await asyncio.sleep(1)
        
        # 4. Verificare le statistiche dopo le conversazioni
        print("\n4. 📊 Statistiche dopo le conversazioni...")
        try:
            async with session.get(f"{BASE_URL}/api/v1/memory/stats") as response:
                if response.status == 200:
                    stats = await response.json()
                    print(f"✅ Utenti attivi: {stats['active_users']}")
                    if stats['users']:
                        for user_id, user_stats in stats['users'].items():
                            print(f"   - Utente {user_id}: {user_stats['message_count']} messaggi")
                else:
                    print(f"❌ Errore statistiche: {response.status}")
        except Exception as e:
            print(f"❌ Errore statistiche: {e}")
        
        # 5. Test pulizia memoria utente specifico
        print("\n5. 🧹 Test pulizia memoria utente specifico (user1)...")
        try:
            clear_request = {"user_id": "user1"}
            async with session.delete(f"{BASE_URL}/api/v1/memory/clear", json=clear_request) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ {data['message']}")
                    print(f"✅ Utenti puliti: {data['users_cleared']}")
                else:
                    print(f"❌ Errore pulizia utente: {response.status}")
                    error_data = await response.text()
                    print(f"❌ Dettagli errore: {error_data}")
        except Exception as e:
            print(f"❌ Errore pulizia utente: {e}")
        
        # 6. Verificare le statistiche dopo la pulizia parziale
        print("\n6. 📊 Statistiche dopo pulizia utente specifico...")
        try:
            async with session.get(f"{BASE_URL}/api/v1/memory/stats") as response:
                if response.status == 200:
                    stats = await response.json()
                    print(f"✅ Utenti attivi: {stats['active_users']}")
                    if stats['users']:
                        for user_id, user_stats in stats['users'].items():
                            print(f"   - Utente {user_id}: {user_stats['message_count']} messaggi")
                else:
                    print(f"❌ Errore statistiche: {response.status}")
        except Exception as e:
            print(f"❌ Errore statistiche: {e}")
        
        # 7. Test pulizia memoria completa
        print("\n7. 🧹 Test pulizia memoria completa (tutti gli utenti)...")
        try:
            clear_request = {}  # Nessun user_id = pulisce tutto
            async with session.delete(f"{BASE_URL}/api/v1/memory/clear", json=clear_request) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ {data['message']}")
                    print(f"✅ Utenti puliti: {data['users_cleared']}")
                else:
                    print(f"❌ Errore pulizia completa: {response.status}")
                    error_data = await response.text()
                    print(f"❌ Dettagli errore: {error_data}")
        except Exception as e:
            print(f"❌ Errore pulizia completa: {e}")
        
        # 8. Statistiche finali
        print("\n8. 📊 Statistiche finali...")
        try:
            async with session.get(f"{BASE_URL}/api/v1/memory/stats") as response:
                if response.status == 200:
                    stats = await response.json()
                    print(f"✅ Utenti attivi: {stats['active_users']}")
                    if stats['users']:
                        for user_id, user_stats in stats['users'].items():
                            print(f"   - Utente {user_id}: {user_stats['message_count']} messaggi")
                    else:
                        print("✅ Nessun utente con conversazioni attive")
                else:
                    print(f"❌ Errore statistiche: {response.status}")
        except Exception as e:
            print(f"❌ Errore statistiche: {e}")
        
        # 9. Test pulizia utente inesistente
        print("\n9. 🧹 Test pulizia utente inesistente...")
        try:
            clear_request = {"user_id": "utente_inesistente"}
            async with session.delete(f"{BASE_URL}/api/v1/memory/clear", json=clear_request) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ {data['message']}")
                    print(f"✅ Utenti puliti: {data['users_cleared']}")
                else:
                    print(f"❌ Errore pulizia utente inesistente: {response.status}")
        except Exception as e:
            print(f"❌ Errore pulizia utente inesistente: {e}")
        
        print("\n" + "=" * 60)
        print("✅ Test completato!")

if __name__ == "__main__":
    print("🚀 Avvio test API memoria conversazioni...")
    print("⚠️  Assicurati che il server MCP sia in esecuzione su http://localhost:8000")
    
    try:
        asyncio.run(test_memory_apis())
    except KeyboardInterrupt:
        print("\n🛑 Test interrotto dall'utente")
    except Exception as e:
        print(f"\n❌ Errore durante i test: {e}")

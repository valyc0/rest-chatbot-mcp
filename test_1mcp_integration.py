#!/usr/bin/env python3
"""
Test script per verificare la connessione al 1MCP Agent
"""

import json
import requests
import asyncio
import aiohttp
from datetime import datetime

async def test_1mcp_agent():
    """Test della connessione al 1MCP Agent"""
    base_url = "http://localhost:3051"
    
    print(f"Testing 1MCP Agent at {base_url}")
    print(f"Time: {datetime.now()}")
    print("-" * 50)
    
    try:
        # Test connessione base
        async with aiohttp.ClientSession() as session:
            # Test health endpoint
            try:
                async with session.get(f"{base_url}/health") as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"✓ Health check passed: {data}")
                    else:
                        print(f"✗ Health check failed: {response.status}")
            except Exception as e:
                print(f"✗ Health check error: {e}")
            
            # Test tools endpoint
            try:
                async with session.get(f"{base_url}/tools") as response:
                    if response.status == 200:
                        tools = await response.json()
                        print(f"✓ Tools available: {len(tools)} tools")
                        for tool in tools[:3]:  # Show first 3 tools
                            print(f"  - {tool.get('name', 'unknown')}: {tool.get('description', 'no description')}")
                    else:
                        print(f"✗ Tools endpoint failed: {response.status}")
            except Exception as e:
                print(f"✗ Tools endpoint error: {e}")
            
            # Test resources endpoint
            try:
                async with session.get(f"{base_url}/resources") as response:
                    if response.status == 200:
                        resources = await response.json()
                        print(f"✓ Resources available: {len(resources)} resources")
                        for resource in resources[:3]:  # Show first 3 resources
                            print(f"  - {resource.get('name', 'unknown')}: {resource.get('uri', 'no uri')}")
                    else:
                        print(f"✗ Resources endpoint failed: {response.status}")
            except Exception as e:
                print(f"✗ Resources endpoint error: {e}")
    
    except Exception as e:
        print(f"✗ Connection failed: {e}")

def test_rest_chatbot_config():
    """Test della configurazione del rest-chatbot-mcp"""
    print("\n" + "="*50)
    print("Testing rest-chatbot-mcp configuration")
    print("="*50)
    
    try:
        with open('mcp_config.json', 'r') as f:
            config = json.load(f)
        
        # Controlla se c'è la configurazione per 1mcp-agent
        mcp_servers = config.get('mcpServers', {})
        
        if '1mcp-agent' in mcp_servers:
            agent_config = mcp_servers['1mcp-agent']
            print(f"✓ 1MCP Agent found in config:")
            print(f"  URL: {agent_config.get('url', 'not set')}")
            print(f"  Headers: {agent_config.get('headers', {})}")
            print(f"  Disabled: {agent_config.get('disabled', False)}")
        else:
            print("✗ 1MCP Agent not found in config")
        
        # Controlla provider
        providers = config.get('providers', {})
        print(f"✓ Providers configured: {list(providers.keys())}")
        
        # Controlla configurazione server
        server_config = config.get('server', {})
        print(f"✓ Server config: {server_config}")
        
    except Exception as e:
        print(f"✗ Config error: {e}")

def test_rest_chatbot_server():
    """Test del server rest-chatbot-mcp"""
    print("\n" + "="*50)
    print("Testing rest-chatbot-mcp server")
    print("="*50)
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Rest-chatbot server is running")
            print(f"  Status: {data.get('status', 'unknown')}")
            print(f"  MCP Available: {data.get('mcp_available', False)}")
        else:
            print(f"✗ Rest-chatbot server returned: {response.status_code}")
    
    except requests.exceptions.ConnectionError:
        print("✗ Rest-chatbot server is not running")
    except Exception as e:
        print(f"✗ Rest-chatbot server error: {e}")

async def main():
    """Main test function"""
    print("=" * 70)
    print("1MCP Agent Integration Test")
    print("=" * 70)
    
    # Test 1MCP Agent
    await test_1mcp_agent()
    
    # Test configurazione
    test_rest_chatbot_config()
    
    # Test server rest-chatbot
    test_rest_chatbot_server()
    
    print("\n" + "=" * 70)
    print("Test completed!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())

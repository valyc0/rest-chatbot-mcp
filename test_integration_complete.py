#!/usr/bin/env python3
"""
Test script to verify the 1MCP Agent integration works correctly
"""

import asyncio
import json
import sys
import os
sys.path.insert(0, '/workspace/db-ready/rest-chatbot-mcp')

from mcp_server import MCPService

async def test_1mcp_integration():
    """Test the 1MCP Agent integration"""
    print("🔄 Testing 1MCP Agent Integration...")
    print("=" * 50)
    
    # Test 1: Configuration loading
    print("1. Testing configuration loading...")
    try:
        service = MCPService('/workspace/db-ready/rest-chatbot-mcp/mcp_config.json')
        config = service.config
        
        if '1mcp-agent' in config.get('mcpServers', {}):
            print("   ✅ 1MCP Agent found in configuration")
            agent_config = config['mcpServers']['1mcp-agent']
            print(f"   📍 URL: {agent_config['url']}")
            print(f"   🔧 Disabled: {agent_config.get('disabled', False)}")
        else:
            print("   ❌ 1MCP Agent not found in configuration")
            return False
    except Exception as e:
        print(f"   ❌ Configuration error: {e}")
        return False
    
    # Test 2: MCP Client creation
    print("\n2. Testing MCP Client creation...")
    try:
        client = service._create_mcp_client()
        print(f"   ✅ Client created: {type(client).__name__}")
        
        # Check if it's using the URL-based configuration
        if hasattr(client, '_config') and client._config:
            print("   ✅ Client has configuration")
        else:
            print("   ⚠️  Client configuration not accessible")
    except Exception as e:
        print(f"   ❌ Client creation error: {e}")
        return False
    
    # Test 3: Service initialization
    print("\n3. Testing service initialization...")
    try:
        success = await service.initialize('openrouter')
        if success:
            print("   ✅ Service initialized successfully")
            print(f"   🤖 Agent type: {type(service.agent).__name__}")
            print(f"   🧠 LLM type: {type(service.llm).__name__}")
        else:
            print("   ❌ Service initialization failed")
            return False
    except Exception as e:
        print(f"   ❌ Service initialization error: {e}")
        return False
    
    # Test 4: Simple query (if possible)
    print("\n4. Testing simple query...")
    try:
        from mcp_server import MCPQueryRequest
        
        request = MCPQueryRequest(
            prompt="Hello, can you tell me what tools are available?",
            provider="openrouter",
            max_steps=1
        )
        
        print("   🔄 Sending test query...")
        response = await service.query(request)
        
        if response.response:
            print(f"   ✅ Query successful!")
            print(f"   📝 Response length: {len(response.response)} chars")
            print(f"   🔢 Steps taken: {response.steps}")
            print(f"   ⏱️  Execution time: {response.execution_time:.2f}s")
            print(f"   📄 Response preview: {response.response[:100]}...")
        else:
            print("   ❌ Query returned empty response")
            return False
            
    except Exception as e:
        print(f"   ❌ Query error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! 1MCP Agent integration is working!")
    return True

if __name__ == "__main__":
    success = asyncio.run(test_1mcp_integration())
    sys.exit(0 if success else 1)

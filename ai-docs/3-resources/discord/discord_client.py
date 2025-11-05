"""Discord integration for confluence charts."""

import asyncio
from datetime import datetime
from pathlib import Path
import discord


async def send_final_decision_embed(channel, decision_msg: dict):
    """Send final architect decision as a Discord embed.

    Args:
        channel: Discord channel object
        decision_msg: Final decision message dict
    """
    from datetime import datetime

    symbol = decision_msg.get("symbol", "Unknown")
    bias = decision_msg.get("bias", "NEUTRAL")
    confidence = decision_msg.get("confidence", 0.0)
    narrative = decision_msg.get("narrative", "")
    price_targets = decision_msg.get("price_targets", [])
    alignment = decision_msg.get("alignment", {})
    timestamp_iso = decision_msg.get("timestamp", datetime.now().isoformat())

    # Parse timestamp
    try:
        dt = datetime.fromisoformat(timestamp_iso.replace('Z', '+00:00'))
        formatted_time = dt.strftime("%A %B %d, %Y @ %I:%M %p ET")
    except:
        formatted_time = datetime.now().strftime("%A %B %d, %Y @ %I:%M %p ET")

    # Title message
    clean_symbol = symbol.replace('/', '')
    aligned_status = "✅ ALIGNED" if alignment.get("aligned", False) else "⚠️ DIVERGENT"
    title_msg = f"🏛️ **{clean_symbol} Final Trading Decision** - {aligned_status}\n{formatted_time}"
    await channel.send(title_msg)
    print(f"   ✅ Sent final decision title")

    # Bias embed
    bias_emoji = {"BULLISH": "📈", "BEARISH": "📉", "NEUTRAL": "↔️"}.get(bias, "❓")
    confidence_pct = int(confidence * 100)

    bias_embed = discord.Embed(
        title=f"{bias_emoji} Final Market Bias: {bias}",
        description=f"**Confidence:** {confidence_pct}%\n**Alignment Score:** {alignment.get('alignment_score', 0.0):.0%}",
        color=0x00ff00 if bias == "BULLISH" else (0xff0000 if bias == "BEARISH" else 0x808080),
        timestamp=datetime.utcnow()
    )

    # Add alignment details
    timeframes = alignment.get('timeframes', [])
    confidence_boost = alignment.get('confidence_boost', 0.0)
    bias_embed.add_field(
        name="📊 Timeframes Analyzed",
        value=", ".join(timeframes) if timeframes else "N/A",
        inline=False
    )
    bias_embed.add_field(
        name="🎯 Alignment Boost",
        value=f"+{confidence_boost:.0%}" if confidence_boost > 0 else "None",
        inline=True
    )

    await channel.send(embed=bias_embed)
    print(f"   ✅ Sent final decision bias card")

    # Narrative (split if too long)
    if narrative:
        # Discord has a 2000 character limit per message
        max_length = 1900
        narrative_parts = [narrative[i:i+max_length] for i in range(0, len(narrative), max_length)]

        for i, part in enumerate(narrative_parts):
            header = "📝 **Master Analysis:**\n" if i == 0 else ""
            await channel.send(f"{header}{part}")
        print(f"   ✅ Sent final decision narrative ({len(narrative_parts)} parts)")

    # Price targets
    if price_targets:
        targets_embed = discord.Embed(
            title="🎯 Multi-Timeframe Price Targets",
            description="Top targets confirmed across multiple timeframes",
            color=0xffd700,
            timestamp=datetime.utcnow()
        )

        for i, target in enumerate(price_targets[:3], 1):
            level_name = target.get("level_name", f"Target {i}")
            price = target.get("price", 0.0)
            distance_pts = target.get("distance_points") or 0.0
            probability = target.get("probability") or 0.0
            priority = target.get("priority", "medium")
            reasoning = target.get("reasoning", "")

            # Get timeframes if available
            timeframes_conf = target.get("timeframes", [])
            tf_text = f"\n**Timeframes:** {', '.join(timeframes_conf)}" if timeframes_conf else ""

            targets_embed.add_field(
                name=f"{i}. {level_name} - {price:.2f}",
                value=f"**Distance:** {abs(distance_pts):.1f} pts | **Probability:** {probability:.0%} | **Priority:** {priority.upper()}{tf_text}\n{reasoning[:150]}",
                inline=False
            )

        await channel.send(embed=targets_embed)
        print(f"   ✅ Sent final decision price targets")


def create_agent_card(agent_info: dict) -> discord.Embed:
    """Create an agent information card embed.

    Args:
        agent_info: Dictionary containing agent details

    Returns:
        discord.Embed: Formatted agent card
    """
    embed = discord.Embed(
        title=f"🤖 {agent_info.get('name', 'AI Agent')}",
        description=agent_info.get('description', 'Smart Money Concepts Analysis Agent'),
        color=0x00ff41,  # Green color for agents
        timestamp=datetime.utcnow()
    )

    # Add model information with descriptive formatting and status
    model_name = agent_info.get('model', 'ollama/llava:13b')
    model_display = f"`{model_name}`"

    if 'tbd' in model_name.lower() or 'to be' in model_name.lower():
        model_display += " 🚧 *(Under Development)*"
    elif 'llava' in model_name.lower():
        model_display += " ✅ *(Vision + Language)*"
    elif 'ollama' in model_name.lower():
        model_display += " ✅ *(Local LLM)*"
    elif 'error' in model_name.lower():
        model_display += " ❌ *(Failed to Load)*"
    else:
        model_display += " ✅ *(Active)*"

    embed.add_field(
        name="🧠 AI Model",
        value=model_display,
        inline=True
    )

    # Add expertise area
    embed.add_field(
        name="🎯 Expertise",
        value=agent_info.get('expertise', 'Institutional Trading Analysis'),
        inline=True
    )

    # Add specialization
    embed.add_field(
        name="📊 Specialization",
        value=agent_info.get('specialization', 'Price Action & Smart Money Concepts'),
        inline=False
    )

    embed.set_footer(text="AI-Powered Market Analysis")
    return embed


async def send_long_message(channel, content: str, max_length: int = 2000):
    """Send a long message by splitting it into chunks if needed.

    Args:
        channel: Discord channel object
        content: Message content
        max_length: Maximum message length (Discord limit is 2000)
    """
    if len(content) <= max_length:
        await channel.send(content)
    else:
        # Split by paragraphs first, then by lines if needed
        chunks = []
        current_chunk = ""

        for paragraph in content.split('\n\n'):
            if len(current_chunk) + len(paragraph) + 2 <= max_length:
                current_chunk += paragraph + '\n\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + '\n\n'

        if current_chunk:
            chunks.append(current_chunk.strip())

        # Send each chunk
        for i, chunk in enumerate(chunks):
            if i == 0:
                await channel.send(chunk)
            else:
                await channel.send(f"**(Continued...)**\n\n{chunk}")


async def send_charts_to_discord(bot_token, channel_id, chart_data, analysis_data=None):
    """Send multiple charts and analyses to Discord in a single async session.

    Args:
        bot_token (str): Discord bot token
        channel_id (str): Discord channel ID
        chart_data (list): List of dicts with 'path', 'title', 'description'
        analysis_data (list, optional): List of markdown analysis strings
    """
    intents = discord.Intents.default()
    intents.message_content = True
    bot = discord.Client(intents=intents)

    @bot.event
    async def on_ready():
        try:
            channel = bot.get_channel(int(channel_id))
            if not channel:
                channel = await bot.fetch_channel(int(channel_id))

            # Send each chart and corresponding analysis
            for i, chart in enumerate(chart_data):
                # Send chart first
                embed = discord.Embed(
                    title=chart['title'],
                    description=chart['description'],
                    color=0x3498db,
                    timestamp=datetime.utcnow()
                )

                file = discord.File(str(chart['path']), filename=chart['path'].name)
                await channel.send(embed=embed, file=file)
                print(f"   ✅ Sent: {chart['path'].name}")

                # Send corresponding analysis if available
                if analysis_data and i < len(analysis_data):
                    analysis = analysis_data[i]

                    # Send agent card first
                    if 'agent_info' in analysis:
                        agent_card = create_agent_card(analysis['agent_info'])
                        await channel.send(agent_card)
                        print(f"   ✅ Sent: Agent card for {analysis['agent_info']['name']}")

                    # Send analysis content (split if too long)
                    analysis_content = analysis.get('markdown', '')
                    if analysis_content:
                        await send_long_message(channel, analysis_content)
                        print(f"   ✅ Sent: Analysis for {chart['title']}")

        except Exception as e:
            print(f"   ❌ Discord error: {e}")
        finally:
            await bot.close()

    await bot.start(bot_token)


async def send_structured_messages_to_discord(bot_token, channel_id, layer_messages):
    """Send structured 5-message format to Discord for each layer.

    Each layer gets 5 messages in sequence:
    1. Title header (text)
    2. Bias & confidence card (embed)
    3. Chart image (embed with file)
    4. Analysis narrative (text)
    5. Price targets (embed)

    Args:
        bot_token (str): Discord bot token
        channel_id (str): Discord channel ID
        layer_messages (list): List of layer message dicts with all data
    """
    intents = discord.Intents.default()
    intents.message_content = True
    bot = discord.Client(intents=intents)

    @bot.event
    async def on_ready():
        try:
            channel = bot.get_channel(int(channel_id))
            if not channel:
                channel = await bot.fetch_channel(int(channel_id))

            # Process each message
            for layer_msg in layer_messages:
                msg_type = layer_msg.get("type", "layer")

                # Handle error messages
                if msg_type == "error":
                    # Send error message
                    await channel.send(f"❌ **Layer {layer_msg['layer_id']} ({layer_msg['layer_name']}) Failed**: {layer_msg['error']}")
                    print(f"   ⚠️ Sent error for Layer {layer_msg['layer_id']}")
                    continue

                # Handle final decision messages
                if msg_type == "final_decision":
                    await send_final_decision_embed(channel, layer_msg)
                    continue

                # Handle regular layer messages
                # Extract layer data
                layer_id = layer_msg["layer_id"]
                layer_name = layer_msg["layer_name"]
                symbol = layer_msg["symbol"]
                timeframe = layer_msg["timeframe"]
                timestamp_iso = layer_msg["timestamp"]
                bias = layer_msg["bias"]
                confidence = layer_msg["confidence"]
                narrative = layer_msg["narrative"]
                price_targets = layer_msg["price_targets"]
                chart_path_str = layer_msg["chart_path"]
                specialization = layer_msg["specialization"]

                # Parse timestamp
                from datetime import datetime
                try:
                    dt = datetime.fromisoformat(timestamp_iso.replace('Z', '+00:00'))
                    formatted_time = dt.strftime("%A %B %d, %Y @ %I:%M %p ET")
                except:
                    formatted_time = datetime.now().strftime("%A %B %d, %Y @ %I:%M %p ET")

                # MESSAGE 1: Title Header
                clean_symbol = symbol.replace('/', '')
                title_msg = f"📊 **{clean_symbol} Analysis - Layer {layer_id} {layer_name}**\n{formatted_time}"
                await channel.send(title_msg)
                print(f"   ✅ Sent title for Layer {layer_id}")

                # MESSAGE 2: Bias & Confidence Card
                bias_emoji = {"BULLISH": "📈", "BEARISH": "📉", "NEUTRAL": "↔️"}.get(bias, "❓")
                confidence_pct = int(confidence * 100)

                bias_embed = discord.Embed(
                    title=f"{bias_emoji} Market Bias",
                    color=0x00ff00 if bias == "BULLISH" else (0xff0000 if bias == "BEARISH" else 0x808080),
                    timestamp=datetime.utcnow()
                )
                bias_embed.add_field(name="Bias", value=bias, inline=True)
                bias_embed.add_field(name="Confidence", value=f"{confidence_pct}%", inline=True)
                bias_embed.add_field(name="AI Model", value="`gemini-2.5-pro`", inline=True)
                bias_embed.add_field(name="Specialization", value=specialization, inline=False)

                await channel.send(embed=bias_embed)
                print(f"   ✅ Sent bias card for Layer {layer_id}")

                # MESSAGE 3: Chart Image
                from pathlib import Path
                chart_path = Path(chart_path_str)

                if chart_path.exists():
                    chart_embed = discord.Embed(
                        title=f"Layer {layer_id} Chart: {layer_name}",
                        description=f"{symbol} {timeframe} - {specialization}",
                        color=0x3498db,
                        timestamp=datetime.utcnow()
                    )

                    file = discord.File(str(chart_path), filename=chart_path.name)
                    await channel.send(embed=chart_embed, file=file)
                    print(f"   ✅ Sent chart for Layer {layer_id}")
                else:
                    await channel.send(f"⚠️ Chart not found: {chart_path_str}")
                    print(f"   ⚠️ Chart missing for Layer {layer_id}")

                # MESSAGE 4: Analysis Narrative
                narrative_msg = f"### 📊 Market Analysis\n\n{narrative}"

                # Split if too long
                await send_long_message(channel, narrative_msg)
                print(f"   ✅ Sent narrative for Layer {layer_id}")

                # MESSAGE 5: Price Targets
                if price_targets:
                    targets_embed = discord.Embed(
                        title="🎯 Price Targets",
                        color=0xffd700,
                        timestamp=datetime.utcnow()
                    )

                    # Group targets by priority
                    high_pri = [t for t in price_targets if t.get("priority") == "high"]
                    med_pri = [t for t in price_targets if t.get("priority") == "medium"]
                    low_pri = [t for t in price_targets if t.get("priority") == "low"]

                    # Format targets by priority
                    for priority_name, targets, emoji in [("HIGH Priority", high_pri, "🔴"), ("MEDIUM Priority", med_pri, "🟡"), ("LOW Priority", low_pri, "🟢")]:
                        if targets:
                            target_text = ""
                            for t in targets[:3]:  # Max 3 per priority
                                level_name = t.get("level_name", "Unknown")
                                price = t.get("price", 0.0)
                                distance_pts = t.get("distance_points") or 0.0
                                distance_adr = t.get("distance_adr_pct") or 0.0
                                prob = t.get("probability") or 0.0
                                reasoning = t.get("reasoning", "")

                                target_text += f"**{level_name}** @ {price:.2f}\n"
                                target_text += f"`{distance_pts:+.2f} pts` | `{distance_adr:+.1f}% ADR` | Prob: {prob:.0%}\n"
                                target_text += f"{reasoning}\n\n"

                            targets_embed.add_field(name=f"{emoji} {priority_name}", value=target_text.strip(), inline=False)

                    await channel.send(embed=targets_embed)
                    print(f"   ✅ Sent price targets for Layer {layer_id}")

                # Add separator between layers
                await channel.send("─" * 50)

        except Exception as e:
            print(f"   ❌ Discord error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await bot.close()

    await bot.start(bot_token)
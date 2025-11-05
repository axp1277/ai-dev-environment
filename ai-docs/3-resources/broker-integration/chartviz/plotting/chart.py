"""Base Chart class for ChartViz plotting engine."""
from typing import Any, Dict, List, Optional

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ..models import (
    Box,
    Candlestick,
    ChartLayout,
    Indicator,
    Level,
    Shade,
    Trade,
    VLine,
)
from ..utils.logging import log_chart_creation, log_debug


class Chart:
    """Core chart class with Plotly figure initialization and layer management."""
    
    def __init__(self, layout: ChartLayout, title: str = "ChartViz"):
        """Initialize chart with layout configuration."""
        self.layout = layout
        self.title = title
        self.fig = self._create_figure()
        self.data_length = 0
        
        log_debug(f"Initialized Chart with title: {title}")
    
    def _create_figure(self) -> go.Figure:
        """Create Plotly figure with configured layout."""
        fig = go.Figure()
        
        # Apply layout configuration
        fig.update_layout(
            title=self.title,
            paper_bgcolor=self.layout.paper_bgcolor,
            plot_bgcolor=self.layout.plot_bgcolor,
            font=dict(
                family=self.layout.font_family,
                size=self.layout.font_size,
                color=self.layout.font_color
            ),
            showlegend=self.layout.showlegend,
            margin=dict(
                l=self.layout.margin.l,
                r=self.layout.margin.r,
                t=self.layout.margin.t,
                b=self.layout.margin.b
            ),
            height=self.layout.height,
            width=self.layout.width
        )
        
        # Configure axes
        fig.update_xaxes(
            showgrid=self.layout.xaxis.showgrid,
            gridcolor=self.layout.xaxis.gridcolor,
            gridwidth=self.layout.xaxis.gridwidth,
            showline=self.layout.xaxis.showline,
            linecolor=self.layout.xaxis.linecolor,
            tickcolor=self.layout.xaxis.tickcolor,
            rangeslider=dict(visible=False)
        )
        
        fig.update_yaxes(
            showgrid=self.layout.yaxis.showgrid,
            gridcolor=self.layout.yaxis.gridcolor,
            gridwidth=self.layout.yaxis.gridwidth,
            showline=self.layout.yaxis.showline,
            linecolor=self.layout.yaxis.linecolor,
            tickcolor=self.layout.yaxis.tickcolor,
            side=self.layout.yaxis.side
        )
        
        return fig
    
    def add_candlesticks(self, df: pd.DataFrame, config: Candlestick) -> None:
        """Add candlestick chart from OHLC data."""
        required_cols = ['open', 'high', 'low', 'close']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"DataFrame must contain columns: {required_cols}")
        
        self.data_length = len(df)
        
        # Use sequential indices to avoid gaps in candlestick chart
        sequential_x = list(range(len(df)))
        
        candlestick = go.Candlestick(
            x=sequential_x,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            increasing_line_color=config.increasing_line_color,
            increasing_fillcolor=config.increasing_fillcolor,
            decreasing_line_color=config.decreasing_line_color,
            decreasing_fillcolor=config.decreasing_fillcolor,
            line=dict(width=config.line_width),
            whiskerwidth=config.whiskerwidth,
            opacity=config.opacity
        )
        
        self.fig.add_trace(candlestick)
        
        # Configure x-axis with datetime labels
        self._configure_datetime_xaxis(df, sequential_x)
        
        log_debug(f"Added candlesticks with {len(df)} bars")
    
    def _configure_datetime_xaxis(self, df: pd.DataFrame, sequential_x: List[int]) -> None:
        """Configure x-axis to show datetime labels with sequential indices."""
        # Convert datetime index to strings for tick labels
        if hasattr(df.index, 'strftime'):
            # If it's a datetime index, format it nicely
            tick_labels = [dt.strftime('%Y-%m-%d %H:%M') for dt in df.index]
        else:
            # If it's not datetime, convert to string
            tick_labels = [str(idx) for idx in df.index]
        
        # Create tick positions - show every nth tick to avoid overcrowding
        n_ticks = min(len(sequential_x), 10)  # Maximum 10 ticks
        if len(sequential_x) > n_ticks:
            tick_step = len(sequential_x) // n_ticks
            tick_positions = list(range(0, len(sequential_x), tick_step))
            tick_texts = [tick_labels[i] for i in tick_positions]
        else:
            tick_positions = sequential_x
            tick_texts = tick_labels
        
        # Update x-axis configuration
        self.fig.update_xaxes(
            tickmode='array',
            tickvals=tick_positions,
            ticktext=tick_texts,
            tickangle=-45  # Rotate labels for better readability
        )
    
    def add_level(self, level: Level) -> None:
        """Add horizontal level line to chart."""
        if self.data_length == 0:
            raise ValueError("Must add candlesticks before adding levels")
        
        end_bar = level.end_bar if level.end_bar is not None else self.data_length - 1
        if level.extend_right:
            end_bar = self.data_length - 1
        
        x_values = [level.start_bar, end_bar]
        y_values = [level.price, level.price]
        
        line_trace = go.Scatter(
            x=x_values,
            y=y_values,
            mode='lines',
            line=dict(
                color=level.color,
                width=level.width,
                dash=level.dash
            ),
            opacity=level.opacity,
            name=level.label,
            showlegend=bool(level.label)
        )
        
        self.fig.add_trace(line_trace)
        
        # Add price label at line end if requested
        if level.show_price_label and level.label:
            label_x = end_bar if level.label_position == "right" else level.start_bar
            # Add small offset for better visibility
            x_offset = 0.5 if level.label_position == "right" else -0.5
            
            self.fig.add_annotation(
                x=label_x + x_offset,
                y=level.price,
                text=level.label,
                showarrow=False,
                xanchor="left" if level.label_position == "right" else "right",
                yanchor="middle",
                bgcolor=level.label_bg_color or level.color,
                bordercolor=level.label_bg_color or level.color,
                font=dict(color=level.label_font_color, size=level.label_font_size),
                opacity=level.opacity
            )
        
        log_debug(f"Added level at price {level.price}")
    
    def add_vline(self, vline: VLine) -> None:
        """Add vertical line to chart spanning full y-axis."""
        if self.data_length == 0:
            raise ValueError("Must add candlesticks before adding vertical lines")
        
        # Get actual y-axis range from ALL chart elements including shapes and annotations
        y_min = float('inf')
        y_max = float('-inf')
        
        # Find y-range from existing traces (candlestick data)
        for trace in self.fig.data:
            if hasattr(trace, 'high') and hasattr(trace, 'low'):
                # Candlestick trace
                y_min = min(y_min, min(trace.low))
                y_max = max(y_max, max(trace.high))
            elif hasattr(trace, 'y') and trace.y is not None:
                # Line trace (Level lines)
                y_values = [y for y in trace.y if y is not None]
                if y_values:
                    y_min = min(y_min, min(y_values))
                    y_max = max(y_max, max(y_values))
        
        # Also check shapes (other horizontal lines that might have been added)
        if hasattr(self.fig, 'layout') and hasattr(self.fig.layout, 'shapes') and self.fig.layout.shapes:
            for shape in self.fig.layout.shapes:
                if hasattr(shape, 'y0') and shape.y0 is not None:
                    y_min = min(y_min, shape.y0)
                if hasattr(shape, 'y1') and shape.y1 is not None:
                    y_max = max(y_max, shape.y1)
        
        # Add some padding to the range
        y_range = y_max - y_min
        y_padding = y_range * 0.05  # 5% padding
        y_min_padded = y_min - y_padding
        y_max_padded = y_max + y_padding
        
        # Add vertical line using shape (not add_vline to avoid auto-scaling issues)
        self.fig.add_shape(
            type="line",
            x0=vline.bar_index,
            x1=vline.bar_index,
            y0=y_min_padded,
            y1=y_max_padded,
            line=dict(
                color=vline.color,
                width=vline.width,
                dash=vline.dash
            ),
            opacity=vline.opacity
        )
        
        # Add label if requested
        if vline.show_label and vline.label:
            label_y = y_max_padded if vline.label_position == "top" else y_min_padded
            y_offset = y_range * 0.02  # Small offset from edge
            if vline.label_position == "top":
                label_y -= y_offset
            else:
                label_y += y_offset
            
            self.fig.add_annotation(
                x=vline.bar_index,
                y=label_y,
                text=vline.label,
                showarrow=False,
                xanchor="center",
                yanchor="bottom" if vline.label_position == "top" else "top",
                bgcolor=vline.label_bg_color or vline.color,
                bordercolor=vline.label_bg_color or vline.color,
                font=dict(color=vline.label_font_color, size=vline.label_font_size),
                opacity=vline.opacity
            )
        
        log_debug(f"Added vertical line at bar {vline.bar_index}")
    
    def add_box(self, box: Box) -> None:
        """Add rectangle/box to chart."""
        if self.data_length == 0:
            raise ValueError("Must add candlesticks before adding boxes")
        
        x1 = box.x1 if box.x1 is not None else self.data_length - 1
        
        shape = dict(
            type="rect",
            x0=box.x0,
            y0=box.y0,
            x1=x1,
            y1=box.y1,
            fillcolor=box.fillcolor,
            line=dict(
                color=box.line_color,
                width=box.line_width,
                dash=box.line_dash
            ),
            opacity=box.opacity,
            layer=box.layer
        )
        
        self.fig.add_shape(**shape)
        
        if box.label:
            self.fig.add_annotation(
                x=(box.x0 + x1) / 2,
                y=(box.y0 + box.y1) / 2,
                text=box.label,
                showarrow=False,
                bgcolor=box.fillcolor,
                bordercolor=box.line_color
            )
        
        log_debug(f"Added box from ({box.x0}, {box.y0}) to ({x1}, {box.y1})")
    
    def add_indicator(self, indicator: Indicator, x_data: Optional[List] = None) -> None:
        """Add technical indicator line to chart."""
        if x_data is None:
            x_data = list(range(len(indicator.values)))
        
        if len(x_data) != len(indicator.values):
            raise ValueError("x_data and indicator values must have same length")
        
        trace = go.Scatter(
            x=x_data,
            y=indicator.values,
            mode=indicator.mode,
            name=indicator.name,
            line=dict(
                color=indicator.color,
                width=indicator.width,
                dash=indicator.dash
            ),
            opacity=indicator.opacity,
            visible=indicator.visible,
            yaxis=indicator.yaxis,
            fill=indicator.fill
        )
        
        self.fig.add_trace(trace)
        log_debug(f"Added indicator {indicator.name} with {len(indicator.values)} points")
    
    def add_shade(self, shade: Shade, indicator1_data: List[float], 
                  indicator2_data: List[float], x_data: Optional[List] = None) -> None:
        """Add shaded area between two indicators."""
        if len(indicator1_data) != len(indicator2_data):
            raise ValueError("Indicator data must have same length")
        
        if x_data is None:
            x_data = list(range(len(indicator1_data)))
        
        # Create filled area between indicators
        trace = go.Scatter(
            x=x_data + x_data[::-1],  # x + x reversed
            y=indicator1_data + indicator2_data[::-1],  # y1 + y2 reversed
            fill='toself',
            fillcolor=shade.fillcolor,
            line=dict(width=shade.line_width),
            opacity=shade.opacity,
            name=f"Shade {shade.indicator1_name}-{shade.indicator2_name}",
            showlegend=False
        )
        
        self.fig.add_trace(trace)
        log_debug(f"Added shade between {shade.indicator1_name} and {shade.indicator2_name}")
    
    def add_trade(self, trade: Trade, x_data: Optional[List] = None) -> None:
        """Add trade visualization with entry/exit markers and connection."""
        if x_data is None:
            x_data = list(range(self.data_length))
        
        # Entry marker
        entry_trace = go.Scatter(
            x=[trade.entry_bar],
            y=[trade.entry_price],
            mode='markers',
            marker=dict(
                symbol=trade.entry_marker.symbol,
                size=trade.entry_marker.size,
                color=trade.entry_marker.color,
                line=dict(
                    width=trade.entry_marker.line_width,
                    color=trade.entry_marker.line_color
                )
            ),
            name=f"Entry {trade.label}" if trade.label else "Entry",
            showlegend=bool(trade.label)
        )
        
        # Exit marker
        exit_trace = go.Scatter(
            x=[trade.exit_bar],
            y=[trade.exit_price],
            mode='markers',
            marker=dict(
                symbol=trade.exit_marker.symbol,
                size=trade.exit_marker.size,
                color=trade.exit_marker.color,
                line=dict(
                    width=trade.exit_marker.line_width,
                    color=trade.exit_marker.line_color
                )
            ),
            name=f"Exit {trade.label}" if trade.label else "Exit",
            showlegend=bool(trade.label)
        )
        
        # Connection line
        connection_trace = go.Scatter(
            x=[trade.entry_bar, trade.exit_bar],
            y=[trade.entry_price, trade.exit_price],
            mode='lines',
            line=dict(
                color=trade.connection_line.color,
                width=trade.connection_line.width,
                dash=trade.connection_line.dash
            ),
            opacity=trade.connection_line.opacity,
            showlegend=False
        )
        
        self.fig.add_trace(entry_trace)
        self.fig.add_trace(exit_trace)
        self.fig.add_trace(connection_trace)
        
        # Add P&L annotation if requested
        if trade.show_pnl:
            pnl = trade.exit_price - trade.entry_price
            pnl_text = f"P&L: {pnl:+.2f}"
            self.fig.add_annotation(
                x=(trade.entry_bar + trade.exit_bar) / 2,
                y=max(trade.entry_price, trade.exit_price) + 0.001,
                text=pnl_text,
                showarrow=False,
                bgcolor="white",
                bordercolor="black"
            )
        
        log_debug(f"Added trade from bar {trade.entry_bar} to {trade.exit_bar}")
    
    def get_figure(self) -> go.Figure:
        """Get the Plotly figure object."""
        return self.fig
    
    def show(self) -> None:
        """Display the chart interactively."""
        self.fig.show()
        
    def to_html(self, file_path: str, **kwargs) -> None:
        """Export chart to HTML file."""
        self.fig.write_html(file_path, **kwargs)
        
    def to_image(self, file_path: str, **kwargs) -> None:
        """Export chart to static image file."""
        self.fig.write_image(file_path, **kwargs)
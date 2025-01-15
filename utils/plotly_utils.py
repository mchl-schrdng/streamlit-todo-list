def apply_transparent_layout(fig):
    """Applies a transparent background layout to a Plotly figure."""
    fig.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",  # Transparent plot area
        paper_bgcolor="rgba(0, 0, 0, 0)",  # Transparent figure background
        font=dict(color="white")           # Text color for visibility
    )
    return fig

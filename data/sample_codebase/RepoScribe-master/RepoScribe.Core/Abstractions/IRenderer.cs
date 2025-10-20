﻿using RepoScribe.Core.ContentItems;

namespace RepoScribe.Core.Abstractions
{
    public interface IRenderer
    {
        string Render(ContentItem contentItem);
    }
}

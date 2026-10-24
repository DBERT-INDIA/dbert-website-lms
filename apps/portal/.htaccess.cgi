# ==============================================================================
# DBERT Internship Portal — Apache CGI Configuration for cPanel
# ==============================================================================
# Use this .htaccess file if running via cgi-bin/dbert.cgi on cPanel.
# Ensure cgi-bin/dbert.cgi has permissions 0755 (chmod 755).

Options +ExecCGI -Indexes
AddHandler cgi-script .cgi

<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /

  # 1. Serve static files (CSS, JS, images, fonts) directly without hitting Python
  RewriteCond %{REQUEST_FILENAME} -f [OR]
  RewriteCond %{REQUEST_FILENAME} -d
  RewriteRule ^ - [L]

  # 2. Exclude cgi-bin from rewrite loop
  RewriteRule ^cgi-bin/ - [L]

  # 3. Dispatch all portal, API, and dynamic routes to dbert.cgi
  RewriteRule ^(.*)$ cgi-bin/dbert.cgi/$1 [L,QSA]
</IfModule>

# Disable Apache output buffering for real-time SSE AI Streaming
<IfModule mod_deflate.c>
  SetEnvIfNoCase Request_URI "/chat$" no-gzip dont-vary
  SetEnvIfNoCase Request_URI "^/courses/.*/chat$" no-gzip dont-vary
</IfModule>

# Browser Caching for Static Assets Only
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType image/png "access plus 1 month"
  ExpiresByType image/jpeg "access plus 1 month"
  ExpiresByType image/svg+xml "access plus 1 month"
</IfModule>

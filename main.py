from app import app
from layout import create_layout
import callbacks  # Imports register the reactive callbacks to the kernel

app.layout = create_layout()

if __name__ == '__main__':
    app.run(debug=True)
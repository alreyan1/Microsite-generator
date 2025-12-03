from app import app, db
from flask import flash, redirect, url_for

@app.route('/test-flash')
def test_flash():
    flash('This is a test message!', 'success')
    flash('This is an error message!', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
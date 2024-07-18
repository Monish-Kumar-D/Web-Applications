document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.edit-button').forEach(button => {
        button.onclick = () => {
            const postId = button.dataset.id;
            const postContent = document.getElementById(`post-content-${postId}`);
            const currentContent = postContent.innerHTML.trim();
            const editForm = document.createElement('textarea');
            editForm.setAttribute('id', `edit-content-${postId}`);
            editForm.style.width = '42vw';
            editForm.value = currentContent;
            postContent.replaceWith(editForm);
            
            const editButton = document.createElement('button');
            editButton.setAttribute('class', 'save-button');
            editButton.setAttribute('data-id', postId);
            editButton.innerText = 'Save';
            button.replaceWith(editButton);
            
            editButton.onclick = () => {
                const newContent = editForm.value;
                fetch(`/edit/${postId}`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: new URLSearchParams({
                        'content': newContent
                    })
                })
                .then(response => response.json())
                .then(result => {
                    if (result.message) {
                        const updatedContent = document.createElement('div');
                        updatedContent.setAttribute('class', 'post-content');
                        updatedContent.setAttribute('id', `post-content-${postId}`);
                        updatedContent.innerHTML = newContent;
                        editForm.replaceWith(updatedContent);
                        
                        const revertButton = document.createElement('button');
                        revertButton.setAttribute('class', 'edit-button');
                        revertButton.setAttribute('data-id', postId);
                        revertButton.innerText = 'Edit';
                        editButton.replaceWith(revertButton);
                        
                        revertButton.onclick = () => {
                            const currentContent = updatedContent.innerHTML.trim();
                            const editForm = document.createElement('textarea');
                            editForm.setAttribute('id', `edit-content-${postId}`);
                            editForm.style.width = '42vw';
                            editForm.value = currentContent;
                            updatedContent.replaceWith(editForm);
                            
                            revertButton.replaceWith(editButton);
                        };
                    } else if (result.error) {
                        alert(result.error);
                    }
                });
            };
        };
    });
    const followButton = document.getElementById('follow-button');
    if (followButton) {
        followButton.onclick = () => {
            const profileId = followButton.dataset.id;
            const isFollowing = followButton.dataset.following === 'true';
            const url = isFollowing ? `/unfollow/${profileId}` : `/follow/${profileId}`;
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            })
            .then(response => response.json())
            .then(result => {
                if (result.message) {
                    followButton.innerText = isFollowing ? 'Follow' : 'Unfollow';
                    followButton.dataset.following = !isFollowing;
                } else if (result.error) {
                    alert(result.error);
                }
            });
        }
    }
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

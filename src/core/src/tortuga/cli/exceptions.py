# Copyright 2008-2018 Univa Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class SkipExecution(Exception):
    """
    This exception, when raised in a pre_execute callable, will cause the
    CLI to stop further execution and exit cleanly without raising a
    user-visible error.

    """
    pass


class SkipPostExecution(Exception):
    """
    This exception, when raised in the execution method, will prevent the
    post_execute callables from running, and exit cleanly without raising a
    user-visible error.

    """
    pass
